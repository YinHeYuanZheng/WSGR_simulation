# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# U-47改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""突袭帕斯卡湾:增加自身耐久 5 点，增加暴击几率 20%。"""


class Skill_111971_1(CommonSkill):
    """增加自身耐久 5 点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='health',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


class Skill_111971_2(Skill):
    """增加暴击几率 20%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.2,
                bias_or_weight=0
            )
        ]


skill = [Skill_111971_1, Skill_111971_2]
