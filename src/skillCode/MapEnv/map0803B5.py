# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-3B点选项5(右下)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0803B5_1(PrepSkill):
    """敌方全体火力+20"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = Target(side=0)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


name = '8-3B点选项5(右下)'
effect = '敌方全体火力+20'
skill = [NormalMap_0803B5_1]
