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

from src.utils.loadConfig import load_config
from src.utils.loadDataset import Dataset
from src.wsgr.wsgrTimer import timer


def run_victory(battle, epoc):
    result = [0] * 6
    resulr_flag_list = ['SS', 'S', 'A', 'B', 'C', 'D']
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        result_flag_id = resulr_flag_list.index(log['result'])
        result[result_flag_id] += 1
        print(f"第{i + 1}次 - 战果分布: "
              f"SS {result[0] / (i + 1) * 100:.2f}%; "
              f"S {result[1] / (i + 1) * 100:.2f}%; "
              f"A {result[2] / (i + 1) * 100:.2f}%; "
              f"B {result[3] / (i + 1) * 100:.2f}%; "
              f"C {result[4] / (i + 1) * 100:.2f}%; "
              f"D {result[5] / (i + 1) * 100:.2f}%; ")


def run_hit_rate(battle, epoc):
    hit_rate = 1
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        hit_rate = (hit_rate * i + log['hit_rate']) / (i + 1)
        print(f"第{i + 1}次 - 命中率: {hit_rate * 100: .4f}%")


def run_avg_damage(battle, epoc):
    avg_damage = 0
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        avg_damage = (avg_damage * i + np.sum(log['create_damage'][1])) / (i + 1)
        print(f"第{i + 1}次 - 平均伤害: {avg_damage:.4f}")


if __name__ == '__main__':
    configDir = os.path.join(os.path.dirname(srcDir), 'config')
    xml_file = os.path.join(configDir, 'config.xml')

    dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
    data_file = os.path.join(dependDir, r'ship\database.xlsx')
    ds = Dataset(data_file)
    timer_init = timer()
    battle = load_config(xml_file, ds, timer_init)

    # run_hit_rate(battle, 1000)
    run_victory(battle, 10000)
