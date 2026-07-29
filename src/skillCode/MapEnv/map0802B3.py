# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-2B点选项3(中间)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0802B3_1(PrepSkill):
    """全队火力、命中-10，回避、装甲+15"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
        ]


name = '8-2B点选项3(中间)'
effect = '全队火力、命中-10，回避、装甲+15'
skill = [NormalMap_0802B3_1]
