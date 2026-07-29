# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-1L点选项2(右上)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0801L2_1(PrepSkill):
    """驱逐回避、对空+10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=DD)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
        ]


name = '8-1L点选项2(右上)'
effect = '驱逐回避、对空+10'
skill = [NormalMap_0801L2_1]
