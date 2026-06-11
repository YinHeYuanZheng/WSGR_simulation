# -*- coding:utf-8 -*-
# Author:银河远征(Agent supported)
# env:py38

import os
import unittest

from src.utils.loadConfig import load_config, load_xml
from src.utils.loadDataset import Dataset
from src.wsgr.wsgrTimer import timer


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))


class BattleIntegrationTest(unittest.TestCase):
    def test_full_battle(self):
        """真实数据库和战斗配置应能完成一场完整战斗。"""
        database_file = os.path.join(
            PROJECT_DIR, 'depend', 'ship', 'database.xlsx'
        )
        config_file = os.path.join(
            PROJECT_DIR, 'config', 'config.xml'
        )
        map_dir = os.path.join(PROJECT_DIR, 'depend', 'map')

        dataset = Dataset(database_file)
        battle_timer = timer()
        battle_config = load_xml(config_file, map_dir)
        battle = load_config(battle_config, map_dir, dataset, battle_timer)

        battle.start()
        report = battle.report()

        self.assertIn(report['result'], ['SS', 'S', 'A', 'B', 'C', 'D'])
        self.assertIn('record', report)
        self.assertGreater(len(report['record']), 0)


if __name__ == '__main__':
    unittest.main()
