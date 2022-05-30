# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 女灶神

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""希望的曙光(3级)：增加自身回避30点，降低自身被攻击概率30%，
战斗结束后，回复上一场战斗损失耐久最多的船只40%的在上一场的受损耐久。"""


class Skill_103071_1(CommonSkill):
    """增加自身回避30点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            )
        ]


class Skill_103071_2(CommonSkill):
    """降低自身被攻击概率30%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            UnMagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.3,
            )
        ]

# todo 战斗后回血


skill = [Skill_103071_1, Skill_103071_2]
