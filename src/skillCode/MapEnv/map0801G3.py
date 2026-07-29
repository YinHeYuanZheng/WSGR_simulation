# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-1G点选项3(中间)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0801G3_1(PrepSkill):
    """全队航速+3，回避-5"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='speed',
                phase=AllPhase,
                value=3,
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


name = '8-1G点选项3(中间)'
effect = '全队航速+3，回避-5'
skill = [NormalMap_0801G3_1]
