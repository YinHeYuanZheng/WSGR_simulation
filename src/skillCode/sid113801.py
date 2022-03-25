# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 圣乔治-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""大舰队(3级)：单纵阵和梯形阵时增加自身火力值12点，降低自身闪避值3点。
T优势提升20%自身炮击战伤害，同航战时提升10%自身炮击战伤害，反航时自身火力不受影响。
"""


class Skill_113801_1(Skill):
    """单纵阵和梯形阵时增加自身火力值12点，降低自身闪避值3点。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                value=12,
                phase=(AllPhase,),
                bias_or_weight=0
            ), StatusBuff(
                timer=timer,
                name='evasion',
                value=-3,
                phase=(AllPhase,),
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return friend.form == 1 or friend.form == 4


class Skill_113801_2(Skill):
    """T优势提升20%自身炮击战伤害，同航战时提升10%自身炮击战伤害，反航时自身火力不受影响。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            FinalDamageBuff_1(
                timer=timer
            ), AtkCoefProcess_1(
                timer=timer
            )
        ]


class FinalDamageBuff_1(FinalDamageBuff):
    """ T优势提升20%自身炮击战伤害，同航战时提升10%自身炮击战伤害"""

    def __init__(self, timer):
        super().__init__(
            timer=timer,
            name='final_damage_buff',
            phase=(ShellingPhase,),
            value=0
        )

    def is_active(self, *args, **kwargs):
        if self.timer.direction_flag == 1:
            self.value = 0.2
            return True
        elif self.timer.direction_flag == 2:
            self.value = 0.1
            return True
        else:
            return False


class AtkCoefProcess_1(AtkCoefProcess):
    """反航时自身火力不受影响"""

    def __init__(self, timer):
        super().__init__(
            timer=timer,
            name='direct_coef',
            phase=(AllPhase,),
            value=1
        )

    def is_active(self, *args, **kwargs):
        return self.timer.direction_flag == 4


skill = [Skill_113801_1, Skill_113801_2]
