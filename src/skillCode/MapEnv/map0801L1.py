# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-1L点选项1(左上)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0801L1_1(PrepSkill):
    """航母火力+10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=CV)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class NormalMap_0801L1_2(PrepSkill):
    """驱逐回避-10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=DD)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            )
        ]


name = '8-1L点选项1(左上)'
effect = '航母火力+10，驱逐回避-10'
skill = [NormalMap_0801L1_1, NormalMap_0801L1_2]
