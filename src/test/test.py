# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import os
import sys
import copy

curDir = os.path.dirname(__file__)
srcDir = os.path.dirname(curDir)
sys.path.append(srcDir)

from src.utils.loadConfig_t import load_config
from src.utils.loadDataset_t import Dataset
from src.wsgr.wsgrTimer import timer


if __name__ == '__main__':
    configDir = os.path.join(os.path.dirname(srcDir), 'config')
    xml_file = os.path.join(configDir, r'config.xml')

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
    damaged = [0] * 4

    return_point = ['B', 'F', 'I']
    return_pos = [0] * 3
    for i in range(3000):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()
        # print(log['record'])

        if log['end_with_boss']:
            result_flag_id = result_flag_list.index(log['result'])
            result[result_flag_id] += 1
            end_flag[0] += 1
        else:
            # 劝退时大破率
            # for tmp_ship in tmp_battle.friend.ship:
            #     if tmp_ship.damaged >= 3:
            #         damaged[tmp_ship.loc - 1] += 1
            # end_flag[1] += 1

            # 劝退位置
            return_pos_id = return_point.index(log['end_with'])
            return_pos[return_pos_id] += 1
            end_flag[1] += 1

        if sum(result) == 0 or end_flag[1] == 0:
            continue

        print(f"第{i+1}次 - boss点战果分布: "
              f"SS {result[0] / sum(result) * 100:.2f}% "
              f"S {result[1] / sum(result) * 100:.2f}% "
              f"A {result[2] / sum(result) * 100:.2f}% "
              f"B {result[3] / sum(result) * 100:.2f}% "
              f"C {result[4] / sum(result) * 100:.2f}% "
              f"D {result[5] / sum(result) * 100:.2f}% "
              f"劝退率 {end_flag[1] / sum(end_flag) * 100:.2f}% "
              f"B {return_pos[0] / sum(return_pos) * 100:.2f}% "
              f"F {return_pos[1] / sum(return_pos) * 100:.2f}% "
              f"I {return_pos[2] / sum(return_pos) * 100:.2f}% "
              # f"大破率 {damaged[0] / end_flag[1] * 100:.2f}% "
              # f"{damaged[1] / end_flag[1] * 100:.2f}% "
              # f"{damaged[2] / end_flag[1] * 100:.2f}% "
              # f"{damaged[3] / end_flag[1] * 100:.2f}%"
              )
