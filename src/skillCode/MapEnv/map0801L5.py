# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-1L点选项5(右下)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0801L5_1(PrepSkill):
    """潜艇鱼雷+10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=SS)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class NormalMap_0801L5_2(PrepSkill):
    """航母、战列火力-5"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=(CV, BB))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            )
        ]


name = '8-1L点选项5(右下)'
effect = '潜艇鱼雷+10，航母、战列火力-5'
skill = [NormalMap_0801L5_1, NormalMap_0801L5_2]
