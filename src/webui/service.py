# -*- coding: utf-8 -*-
# Author:银河远征(AI supported)
"""Application service used by the browser WebUI.

The module deliberately contains no HTTP or DOM code.  It adapts the existing
dataset/configuration loaders and battle engine into JSON-friendly metadata and
simulation snapshots.
"""

from __future__ import annotations

import copy
import multiprocessing as mp
from queue import Empty
import sys
import threading
import time
from pathlib import Path
from typing import Any

import numpy as np
import yaml

from src import skillCode
from src.utils.loadConfig import load_config, load_friend_ship, load_xml
from src.utils.loadDataset import Dataset
from src.utils.runUtil import set_supply
from src.utils.battleUtil import CustomBattle
from src.wsgr.ship import Fleet
from src.wsgr.wsgrTimer import PHASE_LABELS, timer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
SAVE_DIR = CONFIG_DIR / "save"
DEPEND_DIR = PROJECT_ROOT / "depend"
MAP_DIR = DEPEND_DIR / "map"
DATA_FILE = DEPEND_DIR / "ship" / "database.xlsx"

FORMATIONS = [
    {"id": 1, "name": "单纵"},
    {"id": 2, "name": "复纵"},
    {"id": 3, "name": "轮形"},
    {"id": 4, "name": "梯形"},
    {"id": 5, "name": "单横"},
]

BATTLE_TYPES = [
    {"id": "NormalBattle", "name": "常规战"},
    {"id": "DaytimeBattle", "name": "昼战"},
    {"id": "NightBattle", "name": "夜战"},
    {"id": "AirBattle", "name": "航空战"},
    {"id": "OnlyAirBattle", "name": "仅航空战"},
    {"id": "CustomBattle", "name": "自定义"},
]

STRATEGIES = {
    "attack": {
        "label": "攻击",
        "items": {
            "雷击熟练": "111", "炮击训练": "112", "拦阻射击": "113",
            "效力射": "211", "数据交互": "212", "弹跳攻击": "213",
            "穿甲航弹": "311", "全甲板突击": "312", "穿甲榴弹": "313",
        },
    },
    "defense": {
        "label": "防御",
        "items": {
            "对海警戒哨": "121", "前哨援护": "122", "过穿": "123",
            "硬化装甲": "221", "编队援护": "222", "防空弹幕": "223",
            "探照灯警戒": "321", "护航援护": "322", "装甲甲板": "323",
        },
    },
    "special": {
        "label": "特殊",
        "items": {
            "大角度规避": "131", "雁行雷击": "132", "交互射击": "231",
            "硬被帽": "232", "炮塔后备弹": "233", "改良被帽弹": "331",
            "照明弹校正": "332", "对空预警": "333",
        },
    },
}

RESULT_FLAGS = ("SS", "S", "A", "B", "C", "D")
PHASE_LABELS = {
    "LongMissilePhase": "先发制人",
    "SupportPhase": "支援攻击",
    "AirPhase": "航空战",
    "FirstMissilePhase": "导弹战",
    "AntiSubPhase": "先制反潜",
    "FirstTorpedoPhase": "先制雷击",
    "FirstShellingPhase": "首轮炮击",
    "SecondShellingPhase": "次轮炮击",
    "SecondTorpedoPhase": "鱼雷战",
    "SecondMissilePhase": "闭幕导弹",
    "NightPhase": "夜战",
}


def _skill_options(skill_ids: list[str]) -> list[dict[str, Any]]:
    options: list[dict[str, Any]] = [{"id": 0, "name": "无技能"}]
    for index, sid in enumerate(skill_ids, start=1):
        if not sid:
            continue
        try:
            name = getattr(skillCode, f"sid{sid}").name
        except (AttributeError, ImportError):
            name = f"技能 {sid}"
        options.append({"id": index, "sid": sid, "name": name})
    return options


def _serializable_number(value: Any, default: int = 0) -> int:
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


class SimulationBusyError(RuntimeError):
    pass


class SimulationManager:
    """Run one simulation job at a time and expose polling-friendly snapshots."""

    def __init__(self, dataset: Dataset):
        self.dataset = dataset
        self._lock = threading.Lock()
        self._stop_event = threading.Event()
        self._process: mp.Process | None = None
        self._collector_thread: threading.Thread | None = None
        self._state_sink: mp.Queue | None = None
        self._active_job_id = 0
        self._completed = 0
        self._target = 0
        self._stop_requested_completed: int | None = None
        self._state = self._initial_state()

    @staticmethod
    def _initial_state() -> dict[str, Any]:
        return {
            "state": "idle",
            "progress": 0,
            "completed": 0,
            "live_completed": 0,
            "live_progress": 0,
            "stop_requested_completed": None,
            "target": 0,
            "message": "等待开始模拟",
            "log": "等待开始模拟",
            "summary": None,
        }

    def snapshot(self) -> dict[str, Any]:
        with self._lock:
            state = copy.deepcopy(self._state)
        if state["state"] in ("running", "stopping"):
            state["live_completed"] = self._completed
            state["live_progress"] = self._completed / max(self._target, 1) * 100
        return state

    def reset(self) -> dict[str, Any]:
        """Discard the current job and forget its result snapshot."""
        with self._lock:
            process = self._process
            running = process is not None and process.is_alive()
        if running:
            self.stop()
        with self._lock:
            self._active_job_id += 1
            self._process = None
            self._completed = 0
            self._target = 0
            self._stop_requested_completed = None
            self._state = self._initial_state()
            return copy.deepcopy(self._state)

    def start(self, battle_config: dict[str, Any], epoch: int, battle_num: int) -> dict[str, Any]:
        epoch = max(1, min(int(epoch), 1_000_000))
        battle_num = max(1, min(int(battle_num), 5))
        with self._lock:
            if self._process is not None and self._process.is_alive():
                raise SimulationBusyError("已有模拟正在运行")
            self._stop_event = threading.Event()
            self._completed = 0
            self._target = epoch
            self._stop_requested_completed = None
            self._active_job_id += 1
            job_id = self._active_job_id
            self._state = {
                "state": "running",
                "progress": 0,
                "completed": 0,
                "live_completed": 0,
                "live_progress": 0,
                "stop_requested_completed": None,
                "target": epoch,
                "message": "正在建立战斗状态",
                "log": "正在建立战斗状态…",
                "summary": None,
            }
            state = copy.deepcopy(self._state)

        context = self._process_context()
        state_queue = context.Queue()
        if context.get_start_method() == "fork":
            process = context.Process(
                target=_run_forked_simulation,
                args=(self, copy.deepcopy(battle_config), epoch, battle_num, state_queue),
                daemon=True,
                name="wsgr-webui-simulation",
            )
        else:
            process = context.Process(
                target=_run_spawned_simulation,
                args=(str(DATA_FILE), copy.deepcopy(battle_config), epoch, battle_num, state_queue),
                daemon=True,
                name="wsgr-webui-simulation",
            )
        process.start()
        with self._lock:
            self._process = process
        self._collector_thread = threading.Thread(
            target=self._collect_process_updates,
            args=(job_id, state_queue, process),
            daemon=True,
            name="wsgr-webui-state-collector",
        )
        self._collector_thread.start()
        return state

    def stop(self) -> dict[str, Any]:
        with self._lock:
            process = self._process
            requested_completed = self._completed
            # The terminated child no longer owns the active job.  This lets a
            # new simulation start immediately instead of waiting for process
            # reaping to finish.
            self._process = None
            self._stop_requested_completed = requested_completed
            self._active_job_id += 1
            self._state["state"] = "stopped"
            self._state["message"] = "模拟已停止"
            self._state["live_completed"] = requested_completed
            self._state["live_progress"] = requested_completed / max(self._target, 1) * 100
            self._state["stop_requested_completed"] = requested_completed
            self._state["completed"] = requested_completed
            self._state["progress"] = self._state["live_progress"]
            state = copy.deepcopy(self._state)
        if process is not None and process.is_alive():
            process.terminate()
            threading.Thread(
                target=self._reap_stopped_process,
                args=(process,),
                daemon=True,
                name="wsgr-webui-process-reaper",
            ).start()
        return state

    @staticmethod
    def _reap_stopped_process(process: mp.Process) -> None:
        process.join(timeout=0.2)
        if process.is_alive():
            process.kill()
            process.join(timeout=0.2)

    @staticmethod
    def _process_context() -> mp.context.BaseContext:
        if sys.platform != "win32" and "fork" in mp.get_all_start_methods():
            return mp.get_context("fork")
        return mp.get_context("spawn")

    def _collect_process_updates(self, job_id: int, state_queue: mp.Queue, process: mp.Process) -> None:
        while process.is_alive() or not state_queue.empty():
            try:
                state = state_queue.get(timeout=0.05)
            except Empty:
                continue
            with self._lock:
                if job_id != self._active_job_id:
                    continue
                self._state = state
                self._completed = state.get("live_completed", state.get("completed", 0))

    def _send_state_to_parent(self) -> None:
        if self._state_sink is None:
            return
        try:
            self._state_sink.put_nowait(copy.deepcopy(self._state))
        except Exception:
            pass

    def _run(self, battle_config: dict[str, Any], epoch: int, battle_num: int) -> None:
        try:
            # On POSIX the WebUI starts simulations with ``fork``.  Without
            # reseeding here, each child inherits the parent's unchanged
            # NumPy RNG state, so repeated runs with the same fleet can replay
            # the exact same first battle and detail log.
            np.random.seed(None)
            skill_messages: list[str] = []
            battle_timer = timer()
            battle = load_config(
                battle_config, str(MAP_DIR), self.dataset, battle_timer,
                log_func=skill_messages.append,
            )
            if self._stop_event.is_set():
                with self._lock:
                    self._state.update({
                        "state": "stopped",
                        "message": "模拟已停止",
                        "log": "模拟已停止",
                    })
                return
            set_supply(battle, battle_num)
            prebattle_info = self._prebattle_info(battle)
            log_prefix = "\n".join([
                "【技能读取】",
                *(skill_messages or ["未配置可读取的技能"]),
                "",
                "【运行信息】",
                "模拟已启动，正在收集运行结果",
                "",
            ])

            friend_names = [ship.status["name"] for ship in battle.friend.ship]
            enemy_names = [ship.status["name"] for ship in battle.enemy.ship]
            result_counts = {flag: 0 for flag in RESULT_FLAGS}
            phase_totals = np.zeros(len(PHASE_LABELS), dtype=float)
            ship_damage_totals = np.zeros(6, dtype=float)
            ship_damage_phase_totals = np.zeros((len(PHASE_LABELS), 6), dtype=float)
            friend_mid_damage_hits = np.zeros(6, dtype=float)
            friend_heavy_damage_hits = np.zeros(6, dtype=float)
            enemy_sink_hits = np.zeros(6, dtype=float)
            enemy_remaining_health_totals = np.zeros(6, dtype=float)
            supply_totals = {key: 0.0 for key in ("oil", "ammo", "steel", "almn", "repeat")}
            flagship_sink_count = 0
            damage_total = 0.0
            damage_samples: list[float] = []
            battle_detail = ""
            battle_detail_info: dict[str, Any] | None = None
            publish_every = max(1, epoch // 100)
            completed = 0

            for index in range(epoch):
                if self._stop_event.is_set():
                    break
                current_battle = copy.deepcopy(battle)
                current_battle.start()
                report = current_battle.report()
                completed = index + 1
                self._completed = completed

                flag = report.get("result", "D")
                if flag not in result_counts:
                    flag = "D"
                result_counts[flag] += 1

                created_damage = np.asarray(report["create_damage"], dtype=float)[:, :6]
                ship_damage = created_damage.sum(axis=0)
                ship_damage_totals += ship_damage
                ship_damage_phase_totals += created_damage
                current_total_damage = float(ship_damage.sum())
                damage_total += current_total_damage
                damage_samples.append(current_total_damage)

                phase_totals += created_damage.sum(axis=1)

                final_state = np.asarray(report["damaged_state"])[-1]
                friend_state = final_state[:len(friend_names)]
                enemy_state = final_state[6:6 + len(enemy_names)]
                friend_mid_damage_hits[:len(friend_names)] += friend_state >= 2
                friend_heavy_damage_hits[:len(friend_names)] += friend_state >= 3
                enemy_sink_hits[:len(enemy_names)] += enemy_state == 4
                enemy_remaining_health_totals[:len(enemy_names)] += [
                    ship.status["health"] for ship in current_battle.enemy.ship
                ]
                flagship_sink_count += int(len(enemy_state) > 0 and enemy_state[0] == 4)

                for key in supply_totals:
                    supply_totals[key] += float(report.get("supply", {}).get(key, 0))
                if not battle_detail:
                    battle_detail = report.get("record", "")
                    battle_detail_info = self._detail_battle_info(current_battle, report)

                if self._stop_event.is_set():
                    break

                # Let the HTTP worker acquire the GIL and set a pending stop event
                # before this simulation thread starts another battle.
                time.sleep(0)
                if self._stop_event.is_set():
                    break

                if completed == 1 or completed % publish_every == 0 or completed == epoch:
                    summary = self._build_summary(
                        completed, result_counts, flagship_sink_count, damage_total, damage_samples,
                        phase_totals, ship_damage_totals, ship_damage_phase_totals, supply_totals,
                        friend_names, enemy_names, friend_mid_damage_hits, friend_heavy_damage_hits,
                        enemy_sink_hits, enemy_remaining_health_totals,
                        battle_detail, battle_detail_info, prebattle_info,
                    )
                    self._publish("running", completed, epoch, summary, log_prefix)

            final_state_name = "stopped" if self._stop_event.is_set() and completed < epoch else "complete"
            summary = self._build_summary(
                completed, result_counts, flagship_sink_count, damage_total, damage_samples,
                phase_totals, ship_damage_totals, ship_damage_phase_totals, supply_totals,
                friend_names, enemy_names, friend_mid_damage_hits, friend_heavy_damage_hits,
                enemy_sink_hits, enemy_remaining_health_totals,
                battle_detail, battle_detail_info, prebattle_info,
            )
            self._publish(final_state_name, completed, epoch, summary, log_prefix)
        except Exception as exc:  # keep the HTTP service alive and report the actual failure
            with self._lock:
                self._state.update({
                    "state": "error",
                    "message": str(exc),
                    "log": f"模拟失败：{exc}",
                })
            self._send_state_to_parent()

    @staticmethod
    def _build_summary(
        completed: int,
        result_counts: dict[str, int],
        flagship_sink_count: int,
        damage_total: float,
        damage_samples: list[float],
        phase_totals: np.ndarray,
        ship_damage_totals: np.ndarray,
        ship_damage_phase_totals: np.ndarray,
        supply_totals: dict[str, float],
        friend_names: list[str],
        enemy_names: list[str],
        friend_mid_damage_hits: np.ndarray,
        friend_heavy_damage_hits: np.ndarray,
        enemy_sink_hits: np.ndarray,
        enemy_remaining_health_totals: np.ndarray,
        battle_detail: str,
        battle_detail_info: dict[str, Any] | None,
        prebattle_info: dict[str, Any],
    ) -> dict[str, Any]:
        divisor = max(completed, 1)
        supply = {key: value / divisor for key, value in supply_totals.items()}
        return {
            "result_counts": result_counts.copy(),
            "win_rate": (result_counts["SS"] + result_counts["S"]) / divisor * 100,
            "flagship_sink_rate": flagship_sink_count / divisor * 100,
            "average_damage": damage_total / divisor,
            "damage_floor_5": float(np.percentile(damage_samples, 5, method="lower")) if damage_samples else 0.0,
            "average_bucket": supply["repeat"],
            "resource_total": supply["oil"] + supply["ammo"] + supply["steel"] + 3 * supply["almn"],
            "phase_damage": [
                {"index": index, "name": PHASE_LABELS.get(phase, phase), "value": float(phase_totals[index] / divisor)}
                for index, phase in enumerate(PHASE_LABELS.keys())
                if phase_totals[index] > 0
            ],
            "ship_damage": [
                {"name": friend_names[index], "value": float(ship_damage_totals[index] / divisor)}
                for index in range(len(friend_names))
            ],
            "ship_damage_by_phase": [
                {
                    "name": PHASE_LABELS.get(phase, phase),
                    "value": float(phase_totals[index] / divisor),
                    "ships": [
                        {"name": friend_names[ship_index], "value": float(ship_damage_phase_totals[index, ship_index] / divisor)}
                        for ship_index in range(len(friend_names))
                    ],
                }
                for index, phase in enumerate(PHASE_LABELS.keys())
            ],
            "supply": supply,
            "friend_mid_damage_rates": [
                {"name": name, "rate": float(friend_mid_damage_hits[index] / divisor * 100)}
                for index, name in enumerate(friend_names)
            ],
            "friend_heavy_damage_rates": [
                {"name": name, "rate": float(friend_heavy_damage_hits[index] / divisor * 100)}
                for index, name in enumerate(friend_names)
            ],
            "enemy_sink_rates": [
                {"name": name, "rate": float(enemy_sink_hits[index] / divisor * 100)}
                for index, name in enumerate(enemy_names)
            ],
            "enemy_remaining_health": [
                {"name": name, "value": float(enemy_remaining_health_totals[index] / divisor)}
                for index, name in enumerate(enemy_names)
            ],
            "prebattle": copy.deepcopy(prebattle_info),
            "battle_detail": battle_detail,
            "battle_detail_info": copy.deepcopy(battle_detail_info),
        }

    @staticmethod
    def _detail_battle_info(battle, report: dict[str, Any]) -> dict[str, Any]:
        """Return the compact status values belonging to the exported detail battle."""
        air_con_flag = report.get("aerial", [None])[0]
        recon_flag = battle.timer.recon_flag
        direction_flag = battle.timer.direction_flag
        return {
            "result": report.get("result"),
            "recon_success": None if recon_flag is None else bool(recon_flag),
            "direction": None if direction_flag is None else int(direction_flag),
            "air_con": None if air_con_flag is None else int(air_con_flag),
        }

    def _publish(
        self,
        state: str,
        completed: int,
        target: int,
        summary: dict[str, Any],
        log_prefix: str,
    ) -> None:
        progress = completed / max(target, 1) * 100
        counts = summary["result_counts"]
        log = log_prefix + (
            f"已完成 {completed:,} / {target:,} 次模拟（{progress:.1f}%）\n"
            + "战果分布："
            + "  ".join(f"{flag} {counts[flag]:,}" for flag in RESULT_FLAGS)
            + f"\n综合胜率：{summary['win_rate']:.2f}%"
            + f"  旗舰击沉：{summary['flagship_sink_rate']:.2f}%"
            + f"  平均伤害：{summary['average_damage']:.1f}"
        )
        if state == "stopped" and self._stop_requested_completed is not None:
            log += (
                f"\n停止请求接收时：{self._stop_requested_completed:,} 次"
                f"  最终完成：{completed:,} 次"
            )
        message = {
            "running": "正在模拟",
            "complete": "模拟完成",
            "stopped": "模拟已停止",
        }[state]
        with self._lock:
            self._state.update({
                "state": state,
                "progress": progress,
                "completed": completed,
                "live_completed": completed,
                "live_progress": progress,
                "target": target,
                "message": message,
                "log": log,
                "summary": summary,
            })
        self._send_state_to_parent()

    @staticmethod
    def _prebattle_info(battle) -> dict[str, Any]:
        """Collect recon and aerial values for the compact result cards."""
        preview_battle = copy.deepcopy(battle)
        preview_battle.start()
        report = preview_battle.report()
        recon_rate, friend_recon, recon_request = report["recon"]
        air_con_flag, aerial_friend, aerial_enemy = report["aerial"]
        if air_con_flag is None:
            air_con_text = "未进行航空战"
        else:
            air_con_info = ["空确", "空优", "均势", "劣势", "丧失"]
            air_con_text = air_con_info[int(air_con_flag) - 1]
        return {
            "recon_rate": int(recon_rate),
            "friend_recon": float(friend_recon),
            "recon_request": float(recon_request),
            "air_con": air_con_text,
            "friend_aerial": float(aerial_friend),
            "enemy_aerial": float(aerial_enemy),
        }


def _run_forked_simulation(
    manager: SimulationManager,
    battle_config: dict[str, Any],
    epoch: int,
    battle_num: int,
    state_queue: mp.Queue,
) -> None:
    manager._state_sink = state_queue
    manager._run(battle_config, epoch, battle_num)


def _run_spawned_simulation(
    data_file: str,
    battle_config: dict[str, Any],
    epoch: int,
    battle_num: int,
    state_queue: mp.Queue,
) -> None:
    manager = SimulationManager(Dataset(data_file))
    manager._state_sink = state_queue
    manager._run(battle_config, epoch, battle_num)


class WebUIService:
    def __init__(self):
        self.dataset = Dataset(str(DATA_FILE))
        self.simulations = SimulationManager(self.dataset)
        self._bootstrap: dict[str, Any] | None = None

    def bootstrap(self) -> dict[str, Any]:
        if self._bootstrap is None:
            self._bootstrap = {
                "formations": FORMATIONS,
                "battle_types": BATTLE_TYPES,
                "custom_phases": [
                    {"id": phase, "name": PHASE_LABELS[phase]}
                    for phase in CustomBattle.phase_names
                ],
                "friend_ships": self._friend_ship_metadata(),
                "enemy_ships": self._enemy_ship_metadata(),
                "equipment": [
                    {"eid": str(eid), "name": str(row["名称"])}
                    for eid, row in self.dataset.equip_data_friend.iterrows()
                ],
                "strategies": {
                    key: {
                        "label": group["label"],
                        "items": [
                            {"name": name, "stid": stid}
                            for name, stid in group["items"].items()
                        ],
                    }
                    for key, group in STRATEGIES.items()
                },
                "config": self.load_default_config(),
            }
        return copy.deepcopy(self._bootstrap)

    def friend_health_limit(self, ship_config: dict[str, Any]) -> dict[str, int]:
        """Calculate a friendly ship's current maximum durability in isolation.

        Health-related effects are local to the ship, so a lightweight pair of
        temporary fleets is sufficient here; no battle phases are started.
        """
        if not isinstance(ship_config, dict):
            raise ValueError("舰船配置必须为对象")

        required = ("cid", "skill")
        missing = [key for key in required if key not in ship_config]
        if missing:
            raise ValueError(f"舰船配置缺少字段：{', '.join(missing)}")

        preview_config = {
            "cid": str(ship_config["cid"]),
            # Only the ship, its selected skill and equipment affect the durability cap.
            # Fixed neutral values keep this preview small and independent from unrelated editor fields.
            "loc": 1,
            "level": 110,
            "affection": 200,
            "skill": int(ship_config["skill"]),
            "equipment": list(ship_config.get("equipment") or []),
            "strategy": [],
        }
        preview_timer = timer()
        friend = Fleet(preview_timer)
        enemy = Fleet(preview_timer)
        friend.set_form(4)
        friend.set_side(1)
        enemy.set_form(4)
        enemy.set_side(0)

        try:
            ship = load_friend_ship(preview_config, self.dataset, preview_timer, log_func=lambda _: None)
            ship.set_master(friend)
            friend.set_ship([ship])
            friend.set_side(1)
            ship.init_skill(friend, enemy)
            ship.init_health()
        except (AttributeError, IndexError, KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"无法计算该舰船的耐久上限：{exc}") from exc

        maximum = max(1, int(ship.status["standard_health"]))
        return {"max_health": maximum}

    def prepare_simulation_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """Drop redundant full-health overrides before a simulation starts."""
        prepared = copy.deepcopy(config)
        friend_fleet = prepared.get("friend_fleet")
        if not isinstance(friend_fleet, dict):
            return prepared

        for ship in friend_fleet.get("ships", []):
            if not isinstance(ship, dict) or ship.get("input_health") is None:
                continue
            maximum = self.friend_health_limit(ship)["max_health"]
            input_health = max(1, int(ship["input_health"]))
            if input_health >= maximum:
                ship.pop("input_health", None)
            else:
                ship["input_health"] = input_health
        return prepared

    def _friend_ship_metadata(self) -> list[dict[str, Any]]:
        ships: list[dict[str, Any]] = []
        for remodeled, frame in ((False, self.dataset.ship_data_0), (True, self.dataset.ship_data_1)):
            for cid, row in frame.iterrows():
                name = str(row["名称"]) + ("-改" if remodeled else "")
                ships.append({
                    "cid": str(cid),
                    "name": name,
                    "type": str(row["舰种"]),
                    "country": str(row["国籍"]),
                    "equip_slots": _serializable_number(row["装备栏"], 4),
                    "skills": _skill_options([str(row["技能1"]), str(row["技能2"])]),
                })
        return ships

    def _enemy_ship_metadata(self) -> list[dict[str, Any]]:
        return [
            {
                "cid": str(cid),
                "name": str(row["名称"]),
                "type": str(row["舰种"]),
                "level": _serializable_number(row["等级"], 110),
                "health": _serializable_number(row["耐久"]),
                "armor": _serializable_number(row["装甲"]),
                "antiair": _serializable_number(row["对空"]),
            }
            for cid, row in self.dataset.ship_data_enemy.iterrows()
        ]

    @staticmethod
    def load_default_config() -> dict[str, Any]:
        return {
            "battle_type": "NormalBattle",
            "friend_fleet": {"side": 1, "form": 4, "ships": []},
            "enemy_fleet": {"side": 0, "form": 4, "ships": []},
        }

    @staticmethod
    def load_uploaded_config(filename: str, content: str) -> dict[str, Any]:
        suffix = Path(filename).suffix.lower()
        if suffix in (".yaml", ".yml"):
            config = yaml.safe_load(content)
            if not isinstance(config, dict):
                raise ValueError("YAML 配置的顶层必须为对象")
            return config
        if suffix == ".xml":
            import tempfile

            temporary_path: str | None = None
            try:
                # Windows cannot reopen a NamedTemporaryFile while its file
                # handle is still open.  Close it before load_xml reads it.
                with tempfile.NamedTemporaryFile(
                    "w", suffix=".xml", encoding="utf-8", delete=False
                ) as file:
                    file.write(content)
                    temporary_path = file.name
                return load_xml(temporary_path, str(MAP_DIR))
            finally:
                if temporary_path:
                    Path(temporary_path).unlink(missing_ok=True)
        raise ValueError("仅支持 .yaml、.yml 或 .xml 配置文件")

    @staticmethod
    def dump_config(config: dict[str, Any]) -> str:
        return yaml.safe_dump(config, allow_unicode=True, sort_keys=False)
