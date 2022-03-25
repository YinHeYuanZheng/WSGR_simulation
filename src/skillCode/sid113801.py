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
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                value=-3,
                phase=(AllPhase,),
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 1 or \
               self.master.get_form() == 4


class Skill_113801_2(Skill):
    """T优势提升20%自身炮击战伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.2,
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_direction() == 1


class Skill_113801_3(Skill):
    """同航战时提升10%自身炮击战伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.1,
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_direction() == 2


class Skill_113801_4(Skill):
    """反航时自身火力不受影响"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            AtkCoefProcess(
                timer=timer,
                name='direct_coef',
                phase=AllPhase,
                value=1,
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_direction() == 3


skill = [Skill_113801_1, Skill_113801_2, Skill_113801_3, Skill_113801_4]
