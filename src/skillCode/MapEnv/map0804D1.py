# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-4D点选项1(左上)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0804D1_1(PrepSkill):
    """全体命中+15，装甲-10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=15,
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


name = '8-4D点选项1(左上)'
effect = '全体命中+15，装甲-10'
skill = [NormalMap_0804D1_1]
