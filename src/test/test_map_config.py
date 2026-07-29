import copy
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import MagicMock

import numpy as np
import yaml

from src.utils import battleUtil
from src.utils.battleUtil import BattleUtil
from src.utils.loadConfig import load_config, load_yaml
from src.utils.loadDataset import Dataset
from src.utils.mapUtil import DefaultUserRules, Point, UserRules
from src.skillCode.MapEnv import load_map_effect, map_effect_options
from src.webui.service import (
    MapSimulationManager,
    calculate_map_enemy_fleet_summary,
)
import src.wsgr.ship as rship
from src.wsgr.wsgrTimer import timer as BattleTimer
from src.wsgr.wsgrTimer import timer


PROJECT_ROOT = Path(__file__).resolve().parents[2]


class MapBattleConfigTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dataset = Dataset(str(PROJECT_ROOT / "depend" / "ship" / "database.xlsx"))
        with (PROJECT_ROOT / "config" / "config_map_test.yaml").open(
            encoding="utf-8"
        ) as file:
            cls.config = yaml.safe_load(file)

    def test_complete_map_battle_runs_from_config(self):
        loaded = load_yaml(
            str(PROJECT_ROOT / "config" / "config_map_test.yaml"),
            str(PROJECT_ROOT / "depend" / "map"),
        )
        self.assertEqual(loaded["map"], {"mapid": "2-1"})
        config = copy.deepcopy(self.config)
        config.pop("user_rules", None)
        battle_map = load_config(
            config,
            str(PROJECT_ROOT / "depend" / "map"),
            self.dataset,
            timer(),
            log_func=lambda _: None,
        )
        battle_map.start()
        report = battle_map.report()

        self.assertEqual(report["map_path"][0], "入口")
        self.assertEqual(report["map_path"][-1], "F")
        self.assertGreaterEqual(report["map_battle_count"], 2)
        self.assertTrue(report["map_node_events"])
        self.assertIn("recon_rate", report["map_node_events"][0])
        self.assertTrue(report["end_with_boss"])

    def test_top_level_user_rules_stop_at_an_unselected_node(self):
        config = copy.deepcopy(self.config)
        config.pop("user_rules", None)
        config.update({
            "selected_nodes": ["入口"],
            "node_defaults": {"formation": 2},
        })
        battle_map = load_config(
            config,
            str(PROJECT_ROOT / "depend" / "map"),
            self.dataset,
            timer(),
            log_func=lambda _: None,
        )

        battle_map.start()
        report = battle_map.report()

        self.assertEqual(report["map_path"][0], "入口")
        self.assertEqual(len(report["map_path"]), 2)
        self.assertEqual(report["end_with"], report["map_path"][-1])
        self.assertEqual(report["map_battle_count"], 0)

    def test_resource_points_adjust_map_supply_without_creating_battles(self):
        map_document = {
            "mapid": "resource-point-test",
            "nodes": [
                {
                    "name": "入口", "kind": "entrance", "level": 0,
                    "battle": {"type": "Entrance", "roundabout": False, "support": False},
                    "enemy_fleets": [],
                },
                {
                    "name": "补给", "kind": "resource_gain", "level": 1,
                    "battle": {
                        "type": "ResourcePoint", "resource": "oil", "amount": 120,
                        "roundabout": False, "support": False,
                    },
                    "enemy_fleets": [],
                },
                {
                    "name": "损耗", "kind": "resource_loss", "level": 4,
                    "battle": {
                        "type": "ResourcePoint", "resource": "oil", "amount": 35,
                        "roundabout": False, "support": False,
                    },
                    "enemy_fleets": [],
                },
            ],
            "routes": [
                {"from": "入口", "to": "补给", "weight": 1, "relation": "all", "conditions": []},
                {"from": "补给", "to": "损耗", "weight": 1, "relation": "all", "conditions": []},
            ],
        }
        config = {
            "battle_type": "Map",
            "friend_fleet": copy.deepcopy(self.config["friend_fleet"]),
            "map": {"mapid": "resource-point-test"},
            "_map_document": map_document,
        }
        battle_map = load_config(
            config, str(PROJECT_ROOT / "depend" / "map"), self.dataset,
            timer(), log_func=lambda _: None,
        )

        battle_map.start()
        report = battle_map.report()

        self.assertEqual(report["map_path"], ["入口", "补给", "损耗"])
        self.assertEqual(report["map_battle_count"], 0)
        self.assertEqual(report["supply"]["oil"], -85)


class MapUserRulesTest(unittest.TestCase):
    def setUp(self):
        self.point = Point('A', 2)
        self.point.set_type(battleUtil.NormalBattle)
        self.point.set_roundabout(True)

    @staticmethod
    def _fleet(*ship_types):
        ships = [ship_type.__new__(ship_type) for ship_type in ship_types]
        return SimpleNamespace(ship=ships)

    def test_node_arguments_override_defaults_and_first_rule_wins(self):
        rules = UserRules({
            'selected_nodes': ['A'],
            'node_defaults': {
                'formation': 3,
                'long_missile': True,
                'round': False,
                'proceed_stop': [1, 2, 2, 2, 2, 2],
                'rules': [
                    ['(SS >= 2) or (DD >= 3) and (CL >= 1)', '5'],
                    ['(SS >= 2)', 'retreat'],
                ],
            },
            'node_args': {'A': {'night': 'flag_alive', 'long_missile': False}},
        }, ['A'])
        self.point.set_user_rules(rules)
        self.point.round_request = rules.settings_for(self.point)['round']
        friend = self._fleet()
        friend.set_form = lambda value: setattr(friend, 'formation', value)
        enemy = self._fleet(rship.SS, rship.SS)
        enemy.ship[0].damaged = 0
        battle_timer = SimpleNamespace(recon_flag=True, map_retreat=False, info=lambda _: None)

        rules.select_initial_formation(self.point, friend)
        rules.apply_recon_decision(self.point, friend, enemy, battle_timer)

        self.assertEqual(friend.formation, 5)
        self.assertFalse(battle_timer.map_retreat)
        self.assertTrue(rules.should_run_night(self.point, enemy))
        self.assertFalse(rules.should_run_long_missile(self.point))
        self.assertEqual(rules.settings_for(self.point)['proceed_stop'][0], 1)

    def test_recon_and_damage_retreat_decisions(self):
        rules = UserRules({
            'selected_nodes': 'all',
            'node_defaults': {
                'formation_if_recon_fails': 4,
                'retreat_if_recon_fails': True,
                'proceed_stop': [1, -1, -1, -1, -1, -1],
            },
        }, ['A'])
        self.point.set_user_rules(rules)
        friend = self._fleet(rship.SS)
        friend.set_form = lambda value: setattr(friend, 'formation', value)
        friend.ship[0].loc = 1
        friend.ship[0].damaged = 2
        battle_timer = SimpleNamespace(recon_flag=False, map_retreat=False, info=lambda _: None)

        rules.apply_recon_decision(self.point, friend, self._fleet(), battle_timer)

        self.assertEqual(friend.formation, 4)
        self.assertTrue(battle_timer.map_retreat)
        self.assertFalse(rules.should_proceed(self.point, friend))

    def test_default_rules_preserve_the_legacy_formation_and_flagship_guard(self):
        rules = DefaultUserRules(['A'])
        self.point.set_user_rules(rules)
        friend = self._fleet(rship.SS, rship.DD)
        friend.set_form = lambda value: setattr(friend, 'formation', value)
        friend.ship[0].loc, friend.ship[0].damaged = 1, 0
        friend.ship[1].loc, friend.ship[1].damaged = 2, 3

        rules.select_initial_formation(self.point, friend)

        self.assertEqual(friend.formation, 2)
        self.assertTrue(rules.should_proceed(self.point, friend))
        self.assertTrue(rules.should_run_long_missile(self.point))

    def test_non_map_battle_always_keeps_long_missile_phase(self):
        battle = BattleUtil(BattleTimer(), None, None)

        self.assertTrue(battle.should_run_long_missile())


class MapEffectTest(unittest.TestCase):
    def test_map_effect_registry_exposes_module_name_and_label(self):
        self.assertIn(
            {
                "id": "map090102",
                "name": "9图封锁战况(削弱后)",
                "effect": "敌方舰队旗舰存活时，为所有非旗舰单位提供10%减伤",
            },
            map_effect_options(),
        )

    def test_point_effect_is_added_once_and_persists_on_timer(self):
        point = Point('A', 2)
        point.add_map_effect(
            'map090102', '9图封锁战况(削弱后)',
            load_map_effect('map090102')[1],
        )
        battle_timer = BattleTimer()

        point.apply_map_effects(battle_timer)
        point.apply_map_effects(battle_timer)

        self.assertEqual(len(battle_timer.env_skill), 1)
        self.assertEqual(battle_timer.map_env_effect_ids, {'map090102'})
        self.assertIn('【地图效果】9图封锁战况(削弱后)', battle_timer.log['record'])

    def test_unknown_map_effect_node_is_rejected(self):
        map_document = {
            "mapid": "invalid-buffs",
            "nodes": [
                {"name": "入口", "kind": "entrance", "level": 0,
                 "battle": {"type": "Entrance"}, "enemy_fleets": []},
            ],
            "routes": [],
            "buffs": {"不存在": ["map090102"]},
        }
        with self.assertRaisesRegex(ValueError, 'Unknown map buff node'):
            from src.utils.mapUtil import MapUtil
            MapUtil(BattleTimer(), map_document, None, SimpleNamespace(ship=[]), log_func=lambda _: None)

    def test_map_effect_yaml_binds_the_effect_to_its_node(self):
        map_document = {
            "mapid": "map-effects",
            "nodes": [
                {"name": "入口", "kind": "entrance", "level": 0,
                 "battle": {"type": "Entrance"}, "enemy_fleets": []},
                {"name": "终点", "kind": "no_battle", "level": 4,
                 "battle": {"type": "MidPoint"}, "enemy_fleets": []},
            ],
            "routes": [{"from": "入口", "to": "终点", "weight": 1}],
            "buffs": {"终点": "map090102"},
        }
        from src.utils.mapUtil import MapUtil
        battle_map = MapUtil(
            BattleTimer(), map_document, None, SimpleNamespace(ship=[]),
            log_func=lambda _: None,
        )

        self.assertEqual(battle_map.point['终点'].map_effects[0][0], 'map090102')


class MapResultStatisticsTest(unittest.TestCase):
    @staticmethod
    def _statistics(visits, battles):
        return {
            "visits": visits,
            "battles": battles,
            "result_counts": {
                "SS": battles, "S": 0, "A": 0, "B": 0, "C": 0, "D": 0,
            },
            "mid_damage": battles,
            "heavy_damage": 0,
            "mid_damage_by_ship": np.array([battles], dtype=float),
            "heavy_damage_by_ship": np.array([0], dtype=float),
            "recon_rate_total": 80.0 * visits,
            "recon_rate_count": visits,
            "roundabout_rate_total": 60.0 * visits,
            "roundabout_rate_count": visits,
        }

    def test_visits_and_battles_use_separate_denominators(self):
        summary = MapSimulationManager._build_map_summary(
            completed=10,
            cleared=0,
            boss_battles=0,
            boss_flagship_sinks=0,
            node_statistics={"A": self._statistics(visits=5, battles=2)},
            friend_ship_names=["测试舰"],
            supply_totals={
                "oil": 0, "ammo": 0, "steel": 0, "almn": 0, "repeat": 0,
            },
            first_record="",
        )
        statistics = summary["node_statistics"][0]

        self.assertEqual(statistics["visits"], 5)
        self.assertEqual(statistics["battles"], 2)
        self.assertEqual(statistics["roundabout_rate"], 60.0)
        self.assertEqual(statistics["result_rates"]["SS"], 100.0)
        self.assertEqual(statistics["mid_damage_rate"], 100.0)

    def test_battle_statistics_are_empty_when_every_visit_roundabouts(self):
        summary = MapSimulationManager._build_map_summary(
            completed=10,
            cleared=0,
            boss_battles=0,
            boss_flagship_sinks=0,
            node_statistics={"A": self._statistics(visits=5, battles=0)},
            friend_ship_names=["测试舰"],
            supply_totals={
                "oil": 0, "ammo": 0, "steel": 0, "almn": 0, "repeat": 0,
            },
            first_record="",
        )
        statistics = summary["node_statistics"][0]

        self.assertEqual(statistics["visits"], 5)
        self.assertEqual(statistics["roundabout_rate"], 60.0)
        self.assertIsNone(statistics["result_rates"]["SS"])
        self.assertIsNone(statistics["mid_damage_rate"])
        self.assertEqual(statistics["mid_damage_ship_rates"], [None])


class RoundaboutEndPhaseTest(unittest.TestCase):
    def test_successful_roundabout_skips_every_end_phase_settlement(self):
        battle = BattleUtil.__new__(BattleUtil)
        battle.timer = SimpleNamespace(
            round_flag=True,
            run_end_skill=MagicMock(),
        )
        battle.supply_cost = MagicMock()

        BattleUtil.end_phase(battle)

        battle.timer.run_end_skill.assert_not_called()
        battle.supply_cost.assert_not_called()


class MapEnemyFleetSummaryTest(unittest.TestCase):
    def test_summary_uses_direct_database_formulas(self):
        class PreviewDataset:
            ships = {
                "cv": {
                    "type": "CVL", "speed": 25, "recon": 40, "fire": 20,
                    "load": [10], "equip": ["fighter"],
                },
                "cl": {
                    "type": "CL", "speed": 35, "recon": 10, "fire": 0,
                    "equip": ["radar"],
                },
            }
            equipment = {
                "fighter": {
                    "type": "Fighter", "recon": 2, "fire": 0, "antiair": 5,
                },
                "radar": {
                    "type": "Radar", "recon": 3, "fire": 0,
                },
            }

            def get_enemy_ship_status(self, cid):
                return copy.deepcopy(self.ships[cid])

            def get_equip_status(self, eid):
                return copy.deepcopy(self.equipment[eid])

        summary = calculate_map_enemy_fleet_summary(
            PreviewDataset(),
            {"ships": [{"cid": "cv"}, {"cid": "cl"}]},
        )

        self.assertEqual(summary["recon"], 55.0)
        self.assertEqual(summary["speed"], 25.0)
        self.assertAlmostEqual(summary["aerial"], np.log(16) * 5)


if __name__ == "__main__":
    unittest.main()
