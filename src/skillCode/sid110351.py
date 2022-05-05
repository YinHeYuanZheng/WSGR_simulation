# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 鸟海-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""第八舰队(3级)：当该舰作为旗舰时，增加全队重巡、轻巡、驱逐（包括雷巡和导驱）的命中值6点，暴击率6%。"""


class Skill_110351(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(CA, CL, DD, CLT, ASDG))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.06,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


skill = [Skill_110351]
