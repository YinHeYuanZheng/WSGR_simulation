# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-3B点选项3(中间)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0803B3_1(PrepSkill):
    """战列火力+20，命中-10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=BB)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=20,
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


name = '8-3B点选项3(中间)'
effect = '战列火力+20，命中-10'
skill = [NormalMap_0803B3_1]
