# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-4H点选项4(左下)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0804H4_1(PrepSkill):
    """小型船装甲+20，命中-20"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=SmallShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-20,
                bias_or_weight=0
            ),
        ]


name = '8-4H点选项4(左下)'
effect = '小型船装甲+20，命中-20'
skill = [NormalMap_0804H4_1]
