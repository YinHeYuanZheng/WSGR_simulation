# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-1G点选项4(左下)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0801G4_1(PrepSkill):
    """全队对空+10，回避-5"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            ),
        ]


name = '8-1G点选项4(左下)'
effect = '全队对空+10，回避-5'
skill = [NormalMap_0801G4_1]
