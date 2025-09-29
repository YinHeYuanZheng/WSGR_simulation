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

from src.utils.loadConfig import load_xml, load_yaml, load_config
from src.utils.loadDataset import Dataset
from src.utils.runUtil import *
from src.wsgr.wsgrTimer import timer
from src.wsgr.formulas import *


def main(infile, epoch, battle_num, fun, **kwargs):
    timer_init = timer()  # 创建时钟
    if infile.endswith('.xml'):
        battleConfig = load_xml(infile, mapDir)
    elif infile.endswith('.yaml'):
        battleConfig = load_yaml(infile, mapDir)
    else:
        raise Exception(f"未许可的文件后缀'{os.path.splitext(infile)[1]}'")
    battle = load_config(battleConfig, mapDir, ds, timer_init)
    set_supply(battle, battle_num)
    fun(battle, epoch, **kwargs)


configDir = os.path.join(os.path.dirname(srcDir), 'config')
dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
data_file = os.path.join(dependDir, r'ship/database.xlsx')
mapDir = os.path.join(dependDir, r'map')
ds = Dataset(data_file)  # 舰船数据

if __name__ == '__main__':
    epoch = 10000
    battle_num = 1  # 战斗轮次
    supportFlag = False  # todo 是否使用支援攻击
    fun = run_victory
    configFile = os.path.join(configDir, r'event\cv_simulation\config_37.yaml')
    # configFile = os.path.join(configDir, r'config.xml')
    main(configFile, epoch, battle_num, fun)

    # for num in [14, 15]:
    #     configFile = os.path.join(configDir, rf'event\c_team\config_{num}.xml')
    #     main(configFile, epoc, battle_num, fun)
    #     print('\n')
