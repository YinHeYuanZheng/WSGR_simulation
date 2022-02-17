# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import os
import sys

curDir = os.path.dirname(__file__)
srcDir = os.path.dirname(curDir)
sys.path.append(srcDir)

from src.utils.loadConfig import load_config
from src.utils.loadDataset import Dataset


if __name__ == '__main__':
    # xml_file = r'F:\文件\WSGR_simulation\config\config.xml'
    configDir = os.path.join(os.path.dirname(srcDir), 'config')
    xml_file = os.path.join(configDir, 'config.xml')

    dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
    data_file = os.path.join(dependDir, r'ship\database.xlsx')
    ds = Dataset(data_file)
    load_config(xml_file, ds)
