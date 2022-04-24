# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 维内托-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""火力+20，命中-6，战斗中免疫第一次被攻击时受到的伤害"""


class Skill_111121_1(CommonSkill):
    """火力+20，命中-6"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-6,
                bias_or_weight=0
            )
        ]


class Skill_111121_2(Skill):
    """战斗中免疫第一次被攻击时受到的伤害。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            SpecialBuff(
                timer=timer,
                name='shield',
                phase=AllPhase,
                exhaust=1)
        ]


skill = [Skill_111121_1, Skill_111121_2]
