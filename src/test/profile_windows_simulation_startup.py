"""Measure WebUI simulation-start latency on Windows.

Run from the repository root:
    python src/test/profile_windows_simulation_startup.py

The script does not modify any configuration.  It reports both isolated
startup stages and the WebUI manager's actual wait time until its first result.
"""

from __future__ import annotations

import copy
import multiprocessing as mp
import sys
import time
from pathlib import Path
from queue import Empty

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.loadConfig import load_config, load_yaml
from src.utils.loadDataset import Dataset
from src.utils.runUtil import set_supply
from src.webui.service import DATA_FILE, MAP_DIR, SimulationManager
from src.wsgr.wsgrTimer import timer


CONFIG_FILE = PROJECT_ROOT / "config" / "config_test.yaml"
REPEAT_COUNT = 3
TIMEOUT_SECONDS = 90


def _milliseconds(seconds: float) -> float:
    return round(seconds * 1_000, 1)


def _profile_spawn_child(dataset: Dataset, battle_config: dict, result_queue) -> None:
    """Run the same setup work as a WebUI child and return stage timings."""
    started = time.perf_counter()
    battle = load_config(
        battle_config,
        str(MAP_DIR),
        dataset,
        timer(),
        log_func=lambda _: None,
    )
    configured = time.perf_counter()
    set_supply(battle, 1)
    SimulationManager._prebattle_info(battle)
    previewed = time.perf_counter()
    first_battle = copy.deepcopy(battle)
    first_battle.start()
    first_battle.report()
    finished = time.perf_counter()
    result_queue.put({
        "load_config_ms": _milliseconds(configured - started),
        "prebattle_ms": _milliseconds(previewed - configured),
        "first_battle_ms": _milliseconds(finished - previewed),
        "child_total_ms": _milliseconds(finished - started),
    })


def profile_spawn_pipeline(dataset: Dataset, battle_config: dict) -> dict[str, float]:
    """Measure child-process bootstrap plus in-child initialisation stages."""
    context = mp.get_context("spawn")
    result_queue = context.Queue()
    process = context.Process(
        target=_profile_spawn_child,
        args=(dataset, copy.deepcopy(battle_config), result_queue),
    )
    started = time.perf_counter()
    process.start()
    try:
        child_result = result_queue.get(timeout=TIMEOUT_SECONDS)
    except Empty as error:
        process.terminate()
        process.join(timeout=2)
        raise RuntimeError("spawn 子进程在限定时间内没有返回计时结果") from error
    finally:
        process.join(timeout=5)
        if process.is_alive():
            process.terminate()
            process.join(timeout=2)
    elapsed = time.perf_counter() - started
    child_result["spawn_to_first_result_ms"] = _milliseconds(elapsed)
    child_result["spawn_bootstrap_estimate_ms"] = round(
        max(0.0, elapsed * 1_000 - child_result["child_total_ms"]), 1
    )
    return child_result


def profile_webui_start(manager: SimulationManager, battle_config: dict) -> float:
    """Measure exactly what a WebUI click waits for: first completed battle."""
    started = time.perf_counter()
    manager.start(copy.deepcopy(battle_config), epoch=1, battle_num=1)
    deadline = started + TIMEOUT_SECONDS
    while time.perf_counter() < deadline:
        state = manager.snapshot()
        if state["state"] == "error":
            raise RuntimeError(f"WebUI 模拟启动失败：{state['message']}")
        if state.get("live_completed", 0) >= 1:
            process = manager._process
            if process is not None:
                process.join(timeout=5)
            return _milliseconds(time.perf_counter() - started)
        time.sleep(0.02)
    manager.stop()
    raise RuntimeError("WebUI 模拟在限定时间内没有完成首场战斗")


def main() -> None:
    if sys.platform != "win32":
        print("提示：该脚本应在 Windows 上运行；当前结果仅用于检查脚本可执行性。")

    started = time.perf_counter()
    dataset = Dataset(str(DATA_FILE))
    dataset_load_ms = _milliseconds(time.perf_counter() - started)

    started = time.perf_counter()
    battle_config = load_yaml(str(CONFIG_FILE), str(MAP_DIR))
    config_read_ms = _milliseconds(time.perf_counter() - started)

    started = time.perf_counter()
    direct_battle = load_config(
        copy.deepcopy(battle_config), str(MAP_DIR), dataset, timer(), log_func=lambda _: None,
    )
    direct_load_config_ms = _milliseconds(time.perf_counter() - started)
    set_supply(direct_battle, 1)
    started = time.perf_counter()
    SimulationManager._prebattle_info(direct_battle)
    direct_prebattle_ms = _milliseconds(time.perf_counter() - started)

    print("\n=== Windows 模拟启动性能 ===")
    print(f"数据集读取 database.xlsx: {dataset_load_ms:.1f} ms")
    print(f"读取战斗配置: {config_read_ms:.1f} ms")
    print(f"当前进程构建战斗: {direct_load_config_ms:.1f} ms")
    print(f"当前进程预览战斗: {direct_prebattle_ms:.1f} ms")

    spawned = profile_spawn_pipeline(dataset, battle_config)
    print("\n--- 独立 spawn 路径 ---")
    print(f"spawn 至首场结果: {spawned['spawn_to_first_result_ms']:.1f} ms")
    print(f"其中 spawn 启动与进程通信（估算）: {spawned['spawn_bootstrap_estimate_ms']:.1f} ms")
    print(f"子进程构建战斗: {spawned['load_config_ms']:.1f} ms")
    print(f"子进程预览战斗: {spawned['prebattle_ms']:.1f} ms")
    print(f"子进程首场战斗: {spawned['first_battle_ms']:.1f} ms")

    manager = SimulationManager(dataset)
    runs = [profile_webui_start(manager, battle_config) for _ in range(REPEAT_COUNT)]
    print("\n--- WebUI 点击开始模拟 ---")
    for index, elapsed in enumerate(runs, start=1):
        print(f"第 {index} 次至首场结果: {elapsed:.1f} ms")
    print(f"平均: {sum(runs) / len(runs):.1f} ms")


if __name__ == "__main__":
    mp.freeze_support()
    main()
