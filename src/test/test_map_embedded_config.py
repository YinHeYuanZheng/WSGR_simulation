import copy
import unittest
from pathlib import Path

import yaml

from src.utils.loadConfig import load_config, load_yaml
from src.utils.loadDataset import Dataset
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
        battle_map = load_config(
            copy.deepcopy(self.config),
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


if __name__ == "__main__":
    unittest.main()
