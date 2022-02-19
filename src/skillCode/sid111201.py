# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 约克城改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
"""萨奇剪(3级)：提升自身10点火力值和航空战25点制空值；制空权劣势和丧失时不降低舰载机伤害，制空权均势、优势和确保时增加舰载机15%伤害。
"""


class Skill_111201_1(CommonSkill):
    """提升自身10点火力值"""
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                name='fire',
                phase=(AllPhase, ),
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_111201_2(Skill):
    """提升航空战25点制空值"""
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='air_con_buff',
                phase=(AirPhase, ),
                value=25,
                bias_or_weight=0
            )
        ]


class Skill_111201_3(Skill):
    """todo 制空权劣势和丧失时不降低舰载机伤害，"""
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [

        ]

    def is_active(self, friend, enemy):
        return self.timer.air_con_flag > 3


class Skill_111201_4(Skill):
    """制空权均势、优势和确保时增加舰载机15%伤害。"""
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='air_atk_buff',
                phase=(AllPhase, ),
                value=0.15,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.timer.air_con_flag <= 3


skill = [Skill_111201_1, Skill_111201_2, Skill_111201_3, Skill_111201_4]
