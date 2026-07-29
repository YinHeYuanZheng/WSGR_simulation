# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-3H点选项1(左上)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0803H1_1(PrepSkill):
    """护卫舰火力、索敌+10，装甲、回避-15"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=CoverShip)
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
                name='recon',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            ),
        ]


name = '8-3H点选项1(左上)'
effect = '护卫舰火力、索敌+10，装甲、回避-15'
skill = [NormalMap_0803H1_1]
