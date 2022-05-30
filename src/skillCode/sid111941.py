# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 大青花鱼

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自己命中值最多 12 点，暴击率最多 12%。"""


class Skill_111941_1(CommonSkill):
    """增加自己命中值最多 12 点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=12,
                bias_or_weight=0,
            )
        ]


class Skill_111941_2(Skill):
    """增加自己暴击率最多 12%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.12,
                bias_or_weight=0,
            )
        ]


skill = [Skill_111941_1, Skill_111941_2]
