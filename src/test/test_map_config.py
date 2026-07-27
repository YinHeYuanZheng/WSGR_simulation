import copy
import unittest
from pathlib import Path
from types import SimpleNamespace

import yaml

from src.utils import battleUtil
from src.utils.battleUtil import BattleUtil
from src.utils.loadConfig import load_config, load_yaml
from src.utils.loadDataset import Dataset
from src.utils.mapUtil import DefaultUserRules, Point, UserRules
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


if __name__ == "__main__":
    unittest.main()
