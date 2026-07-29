# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-4D点选项5(右下)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0804D5_1(PrepSkill):
    """全体火力、装甲+15，闪避、命中-10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
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
            StatusBuff(
                timer=timer,
                name='evasion',
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
        ]


name = '8-4D点选项5(右下)'
effect = '全体火力、装甲+15，闪避、命中-10'
skill = [NormalMap_0804D5_1]
