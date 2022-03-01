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
    # xml_file = r'F:\文件\WSGR_simulation\config\config.xml'
    configDir = os.path.join(os.path.dirname(srcDir), 'config')
    xml_file = os.path.join(configDir, 'config.xml')

    dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
    data_file = os.path.join(dependDir, r'ship\database.xlsx')
    ds = Dataset(data_file)
    timer_init = timer()
    battle = load_config(xml_file, ds, timer_init)
    hit_rate = 1
    for i in range(5000):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.battle_start()
        hit_rate = (hit_rate * i + tmp_battle.report()) / (i + 1)
        print(f"第{i+1}次：平均命中率 {hit_rate * 100}%")
