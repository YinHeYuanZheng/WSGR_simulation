# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-3H点选项5(右下)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0803H5_1(PrepSkill):
    """敌方护卫舰闪避+10，装甲+10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=0, shiptype=CoverShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
        ]


name = '8-3H点选项5(右下)'
effect = '敌方护卫舰闪避+10，装甲+10'
skill = [NormalMap_0803H5_1]
