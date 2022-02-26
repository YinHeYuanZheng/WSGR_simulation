# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# G15-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
"""增加自身火力值15点、航速3节。
航空战阶段自身被攻击概率提高40%，受到伤害减少15点。"""


class Skill_104861_1(CommonSkill):
    """增加自身火力值15点、航速3节。"""
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0,
            ),
            CommonBuff(
                name='speed',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            )
        ]


class Skill_104861_2(Skill):
    # todo 航空战嘲讽
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = []


class Skill_104861_3(Skill):
    """航空战阶段自身受到伤害减少15点"""
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='reduce_damage',
                phase=(AirPhase,),
                value=15,
                bias_or_weight=0
            )
        ]


skill = [Skill_104861_1, Skill_104861_3]
