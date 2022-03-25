# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 黎塞留-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自己命中值10点，回避10点。反航战时，自己攻击造成的最终伤害提高40%。T劣时，自己攻击造成的最终伤害提高70%。"""


class Skill_111131(Skill):

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ), StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ), FinalDamageBuff_1(
                timer=timer
            ), FinalDamageBuff_2(
                timer=timer
            )
        ]


class FinalDamageBuff_1(FinalDamageBuff):
    def __init__(self, timer):
        super().__init__(timer=timer,
                         name='final_damage_buff',
                         phase=AllPhase,
                         value=0.4
                         )

    def is_active(self, *args, **kwargs):
        return self.timer.direction_flag == 3


class FinalDamageBuff_2(FinalDamageBuff):
    def __init__(self, timer):
        super().__init__(timer=timer,
                         name='final_damage_buff',
                         phase=AllPhase,
                         value=0.7
                         )

    def is_active(self, *args, **kwargs):
        return self.timer.direction_flag == 4


Skill = [Skill_111131]
