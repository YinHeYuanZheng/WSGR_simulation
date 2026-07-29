# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-2B点选项4(左下)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0802B4_1(PrepSkill):
    """全队命中+20，回避、装甲-10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            ),
        ]


name = '8-2B点选项4(左下)'
effect = '全队命中+20，回避、装甲-10'
skill = [NormalMap_0802B4_1]
