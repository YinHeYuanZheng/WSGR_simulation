# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-1G点选项1(左上)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0801G1_1(PrepSkill):
    """全队索敌+5，火力-5"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            ),
        ]


name = '8-1G点选项1(左上)'
effect = '全队索敌+5，火力-5'
skill = [NormalMap_0801G1_1]
