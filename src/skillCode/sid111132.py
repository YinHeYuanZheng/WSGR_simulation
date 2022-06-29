# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 黎塞留-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自己命中值10点，回避10点。
反航战时，自己攻击造成的最终伤害提高40%。
T劣时，自己攻击造成的最终伤害提高70%。"""


class Skill_111132_1(CommonSkill):
    """增加自己命中值10点，回避10点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_111132_2(Skill):
    """反航战时，自己攻击造成的最终伤害提高40%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.4
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_dir_flag() == 3


class Skill_111132_3(Skill):
    """T劣时，自己攻击造成的最终伤害提高70%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.7
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_dir_flag() == 4


skill = [Skill_111132_1, Skill_111132_2, Skill_111132_3]
