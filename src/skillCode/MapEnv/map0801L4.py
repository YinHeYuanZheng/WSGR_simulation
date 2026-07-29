# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-1L点选项4(左下)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0801L4_1(PrepSkill):
    """轻巡和重巡火力、命中+10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=(CL, CA))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
        ]


name = '8-1L点选项4(左下)'
effect = '轻巡和重巡火力+10，命中+10'
skill = [NormalMap_0801L4_1]
