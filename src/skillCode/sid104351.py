# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# B65-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""当自身为旗舰时，炮击战阶段提升全队中、小型船 10 点回避值，
夜战阶段提升中型船 13 点火力值和小型船 10 点鱼雷值"""


class Skill_104351_1(Skill):
    """当自身为旗舰时，炮击战阶段提升全队中 10 点回避值，夜战阶段提升中型船 13 点火力值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=MidShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=ShellingPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=NightPhase,
                value=13,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


class Skill_104351_2(Skill):
    """当自身为旗舰时，炮击战阶段提升全队小型船 10 点回避值，夜战阶段提升小型船 10 点鱼雷值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=SmallShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=ShellingPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=NightPhase,
                value=10,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


skill = [Skill_104351_1, Skill_104351_2]
