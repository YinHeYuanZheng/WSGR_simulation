# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-2封锁战况(削弱后)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_080202_1(PrepSkill):
    """战列、战巡火力、装甲-10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=(BB, BC))
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
                name='armor',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            ),
        ]


name = '8-2封锁战况(削弱后)'
effect = '战列、战巡火力、装甲-10'
skill = [NormalMap_080202_1]
