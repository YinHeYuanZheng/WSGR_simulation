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


def main(xml_file, epoc, battle_num, fun):
    timer_init = timer()  # 创建时钟
    battle = load_config(xml_file, mapDir, ds, timer_init)
    set_supply(battle, battle_num)
    fun(battle, epoc)


configDir = os.path.join(os.path.dirname(srcDir), 'config')
dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
data_file = os.path.join(dependDir, r'ship\database.xlsx')
mapDir = os.path.join(dependDir, r'map')
ds = Dataset(data_file)  # 舰船数据

if __name__ == '__main__':
    epoc = 3000
    battle_num = 1  # 战斗轮次
    fun = run_victory
    # xml_file = os.path.join(configDir, r'event\event04\config_10.xml')
    # main(xml_file, epoc, battle_num, fun)

    for num in [5]:
        xml_file = os.path.join(configDir, rf'event\event05\config_{num}.xml')
        main(xml_file, epoc, battle_num, fun)
        print('\n')
