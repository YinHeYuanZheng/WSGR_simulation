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
    xml_file = os.path.join(configDir, r'event\event2\config_4_1.xml')

    dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
    data_file = os.path.join(dependDir, r'ship\database.xlsx')
    ds = Dataset(data_file)  # 舰船数据

    mapDir = os.path.join(dependDir, r'map')
    timer_init = timer()  # 创建时钟
    battle = load_config(xml_file, mapDir, ds, timer_init)

    # print(battle.friend.ship)

    result = [0] * 6
    result_flag_list = ['SS', 'S', 'A', 'B', 'C', 'D']
    end_flag = [0] * 2

    return_pos = [0] * 3
    enemy_rest = [0] * 6
    for i in range(1000):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        result_flag_id = result_flag_list.index(log['result'])
        result[result_flag_id] += 1
        # print(log['record'])

        for j in range(6):
            if tmp_battle.enemy.ship[j].damaged < 4:
                enemy_rest[j] += 1

        print(f"第{i+1}次 - "
              # f"boss点战果分布: "
              # f"SS {result[0] / sum(result) * 100:.2f}% "
              # f"S {result[1] / sum(result) * 100:.2f}% "
              # f"A {result[2] / sum(result) * 100:.2f}% "
              # f"B {result[3] / sum(result) * 100:.2f}% "
              # f"C {result[4] / sum(result) * 100:.2f}% "
              # f"D {result[5] / sum(result) * 100:.2f}% "
              f"刁民率 "
              f"{enemy_rest[0] / (i + 1) * 100:.2f}% "
              f"{enemy_rest[1] / (i + 1) * 100:.2f}% "
              f"{enemy_rest[2] / (i + 1) * 100:.2f}% "
              f"{enemy_rest[3] / (i + 1) * 100:.2f}% "
              f"{enemy_rest[4] / (i + 1) * 100:.2f}% "
              f"{enemy_rest[5] / (i + 1) * 100:.2f}% "
              )
