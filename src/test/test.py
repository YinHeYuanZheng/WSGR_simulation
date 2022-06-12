# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import os
import sys
import copy
import numpy as np

curDir = os.path.dirname(__file__)
srcDir = os.path.dirname(curDir)
sys.path.append(srcDir)

from src.test.loadConfig_t import load_config
from src.test.loadDataset_t import Dataset
from src.wsgr.wsgrTimer import timer


if __name__ == '__main__':
    configDir = os.path.join(os.path.dirname(srcDir), 'config')
    xml_file = os.path.join(configDir, r'event\event03\config_1.xml')

    dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
    data_file = os.path.join(dependDir, r'ship\database.xlsx')
    ds = Dataset(data_file)  # 舰船数据

    mapDir = os.path.join(dependDir, r'map')
    timer_init = timer()  # 创建时钟
    battle = load_config(xml_file, mapDir, ds, timer_init)

    print(battle.friend.ship)

    result = [0] * 6
    result_flag_list = ['SS', 'S', 'A', 'B', 'C', 'D']
    end_flag = [0] * 2
    # supply = {'oil': 0, 'ammo': 0, 'steel': 0, 'almn': 0}
    # avg_damage = 0
    for i in range(1000):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()
        # print(log['record'])

        if log['end_with_boss']:
            result_flag_id = result_flag_list.index(log['result'])
            result[result_flag_id] += 1
            end_flag[0] += 1
        else:
            end_flag[1] += 1

        # supply['oil'] += log['supply']['oil']
        # supply['ammo'] += log['supply']['ammo']
        # supply['steel'] += log['supply']['steel']
        # supply['almn'] += log['supply']['almn']

        # avg_damage += np.sum(log['got_damage'][0])

        if sum(result) == 0:
            continue

        print(f"第{i+1}次 - boss点战果分布: "
              f"SS {result[0] / sum(result) * 100:.2f}% "
              f"S {result[1] / sum(result) * 100:.2f}% "
              f"A {result[2] / sum(result) * 100:.2f}% "
              f"B {result[3] / sum(result) * 100:.2f}% "
              f"C {result[4] / sum(result) * 100:.2f}% "
              f"D {result[5] / sum(result) * 100:.2f}% "
              f"劝退率 {end_flag[1] / sum(end_flag) * 100:.2f}"
              # f"平均有效伤害: {avg_damage / (i + 1):.3f}"
              )
