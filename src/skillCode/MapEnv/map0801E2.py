# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-1E点选项2(右上)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0801E2_1(PrepSkill):
    """全队装甲、回避+10，火力-10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            ),
        ]


name = '8-1E点选项2(右上)'
effect = '全队装甲、回避+10，火力-10'
skill = [NormalMap_0801E2_1]
