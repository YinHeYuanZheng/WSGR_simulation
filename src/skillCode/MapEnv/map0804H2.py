# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-4H点选项2(右上)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0804H2_1(PrepSkill):
    """航母暴击率+10%，闪避-20"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=CV)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-20,
                bias_or_weight=0
            ),
        ]


name = '8-4H点选项2(右上)'
effect = '航母暴击率+10%，闪避-20'
skill = [NormalMap_0804H2_1]
