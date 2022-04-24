# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 加利福尼亚-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""降低自身命中值5点，提升自身15%暴击率。战斗全阶段每受到一次攻击(含未命中)，提升自身火力值13点。"""


class Skill_111071_1(CommonSkill):
    """降低自身命中值5点，"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            )
        ]


class Skill_111071_2(Skill):
    """提升自身15%暴击率"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0
            )
        ]


class Skill_111071_3(Skill):
    """战斗全阶段每受到一次攻击(含未命中)，提升自身火力值13点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
           AtkHitBuff(
               timer=timer,
               name='get_atk',
               phase=AllPhase,
               buff=[
                   StatusBuff(
                       timer=timer,
                       name='fire',
                       phase=AllPhase,
                       value=13,
                       bias_or_weight=0
                   )
               ],
               side=1
           )
        ]


skill = [Skill_111071_1, Skill_111071_2, Skill_111071_3]
