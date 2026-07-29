# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-1L点选项3(中间)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0801L3_1(PrepSkill):
    """战列火力+10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=BB)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class NormalMap_0801L3_2(PrepSkill):
    """航母火力-10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=CV)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            )
        ]


name = '8-1L点选项3(中间)'
effect = '战列火力+10，航母火力-10'
skill = [NormalMap_0801L3_1, NormalMap_0801L3_2]
