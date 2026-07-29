# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-4H点选项5(右下)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0804H5_1(PrepSkill):
    """护卫舰闪避+20，装甲-20"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=CoverShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-20,
                bias_or_weight=0
            ),
        ]


name = '8-4H点选项5(右下)'
effect = '护卫舰闪避+20，装甲-20'
skill = [NormalMap_0804H5_1]
