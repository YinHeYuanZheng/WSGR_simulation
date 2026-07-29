# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-3H点选项4(左下)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0803H4_1(PrepSkill):
    """敌方主力舰命中+10，火力+5"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=0, shiptype=MainShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
        ]


name = '8-3H点选项4(左下)'
effect = '敌方主力舰命中+10，火力+5'
skill = [NormalMap_0803H4_1]
