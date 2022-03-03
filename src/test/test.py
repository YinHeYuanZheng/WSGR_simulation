# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import os
import sys
import copy

curDir = os.path.dirname(__file__)
srcDir = os.path.dirname(curDir)
sys.path.append(srcDir)

from src.utils.loadConfig import load_config
from src.utils.loadDataset import Dataset
from src.wsgr.wsgrTimer import timer


if __name__ == '__main__':
    configDir = os.path.join(os.path.dirname(srcDir), 'config')
    xml_file = os.path.join(configDir, 'config.xml')

    dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
    data_file = os.path.join(dependDir, r'ship\database.xlsx')
    ds = Dataset(data_file)
    timer_init = timer()
    battle = load_config(xml_file, ds, timer_init)

    result = [0] * 6
    resulr_flag_list = ['SS', 'S', 'A', 'B', 'C', 'D']
    for i in range(1000):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()

        log = tmp_battle.report()
        result_flag_id = resulr_flag_list.index(log['result'])
        result[result_flag_id] += 1
        print(f"第{i+1}次 - 战果分布: SS {result[0] / (i + 1) * 100:.1f}%; "
              f"S {result[1] / (i + 1) * 100:.1f}%; "
              f"A {result[2] / (i + 1) * 100:.1f}%; "
              f"B {result[3] / (i + 1) * 100:.1f}%; "
              f"C {result[4] / (i + 1) * 100:.1f}%; "
              f"D {result[5] / (i + 1) * 100:.1f}%; ")
