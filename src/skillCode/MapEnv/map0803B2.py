# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-3B点选项2(右上)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0803B2_1(PrepSkill):
    """重巡火力+20，装甲-15"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=CA)
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
                name='armor',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            ),
        ]


name = '8-3B点选项2(右上)'
effect = '重巡火力+20，装甲-15'
skill = [NormalMap_0803B2_1]
