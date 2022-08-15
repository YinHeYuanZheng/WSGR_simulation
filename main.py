# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import os
import sys
import copy
import numpy as np

curDir = os.path.dirname(__file__)
srcDir = os.path.join(curDir, 'src')
sys.path.append(srcDir)

from src.utils.loadConfig_t import load_config
from src.utils.loadDataset_t import Dataset
from src.wsgr.wsgrTimer import timer


def run_victory(battle, epoc):
    result = [0] * 6
    result_flag_list = ['SS', 'S', 'A', 'B', 'C', 'D']
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        result_flag_id = result_flag_list.index(log['result'])
        result[result_flag_id] += 1
        print(f"第{i + 1}次 - 战果分布: "
              f"SS {result[0] / (i + 1) * 100:.2f}% "
              f"S {result[1] / (i + 1) * 100:.2f}% "
              f"A {result[2] / (i + 1) * 100:.2f}% "
              f"B {result[3] / (i + 1) * 100:.2f}% "
              f"C {result[4] / (i + 1) * 100:.2f}% "
              f"D {result[5] / (i + 1) * 100:.2f}% ")


def run_hit_rate(battle, epoc):
    hit_rate = 0
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        hit_rate += log['hit_rate']
        print(f"第{i + 1}次 - 命中率: {hit_rate / (i + 1) * 100: .4f}%")


def run_avg_damage(battle, epoc):
    avg_damage = 0
    retreat_num = 0
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        avg_damage += np.sum(log['create_damage'][1])
        retreat_num += log['enemy_retreat_num']
        print(f"第{i + 1}次 - 平均伤害: {avg_damage / (i + 1):.3f}; "
              f"平均击沉 {retreat_num / (i + 1):.2f}")


def run_supply_cost(battle, epoc):
    supply = {'oil': 0, 'ammo': 0, 'steel': 0, 'almn': 0}
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        supply['oil'] += log['supply']['oil']
        supply['ammo'] += log['supply']['ammo']
        supply['steel'] += log['supply']['steel']
        supply['almn'] += log['supply']['almn']
        print(f"第{i + 1}次 - 资源消耗: "
              f"油 {supply['oil'] / (i + 1):.1f}, "
              f"弹 {supply['ammo'] / (i + 1):.1f}, "
              f"钢 {supply['steel'] / (i + 1):.1f}, "
              f"铝 {supply['almn'] / (i + 1):.1f}.")


if __name__ == '__main__':
    configDir = os.path.join(os.path.dirname(srcDir), 'config')
    xml_file = os.path.join(configDir, r'event\config_11.xml')

    dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
    data_file = os.path.join(dependDir, r'ship\database.xlsx')
    ds = Dataset(data_file)  # 舰船数据

    mapDir = os.path.join(dependDir, r'map')
    timer_init = timer()  # 创建时钟
    battle = load_config(xml_file, mapDir, ds, timer_init)
    del ds

    # run_hit_rate(battle, 1000)
    run_victory(battle, 1000)
    # run_avg_damage(battle, 10000)
    # run_supply_cost(battle, 1000)
