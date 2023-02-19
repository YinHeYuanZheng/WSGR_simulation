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
from src.utils.runUtil import *
from src.wsgr.wsgrTimer import timer
from src.wsgr.formulas import *


if __name__ == '__main__':
    configDir = os.path.join(os.path.dirname(srcDir), 'config')
    xml_file = os.path.join(configDir, r'event\event04\config_3.xml')
    dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
    data_file = os.path.join(dependDir, r'ship\database.xlsx')
    ds = Dataset(data_file)  # 舰船数据

    mapDir = os.path.join(dependDir, r'map')
    timer_init = timer()  # 创建时钟
    battle = load_config(xml_file, mapDir, ds, timer_init)
    del ds

    set_supply(battle, 4)
    # for accuracy in np.arange(100, 201, 50):
    #     print(f"accuracy: {accuracy}")
    #     for ship in battle.enemy.ship:
    #         ship.status['accuracy'] = accuracy
    run_victory(battle, 5000)
    # for hit_rate in np.arange(0.5, 1, 0.05):
    #     hit_rate = np.round(hit_rate, 2)
    #     print(f"hit_rate: {hit_rate}")
    #     NormalAtk.outer_hit_verify = new_hit_verify(hit_rate)
    #     run_damaged(battle, 1000)
