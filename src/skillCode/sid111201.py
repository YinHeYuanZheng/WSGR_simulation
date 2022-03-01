# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 约克城改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""萨奇剪(3级)：提升自身10点火力值和航空战25点制空值；
制空权劣势和丧失时不降低舰载机伤害，
制空权均势、优势和确保时增加舰载机15%伤害。
"""


class Skill_111201_1(CommonSkill):
    """提升自身10点火力值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=(AllPhase, ),
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_111201_2(Skill):
    """提升航空战25点制空值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_con_buff',
                phase=(AirPhase,),
                value=25,
                bias_or_weight=0
            )
        ]


class Skill_111201_3(Skill):
    """制空权劣势和丧失时不降低舰载机伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkCoefProcess(
                timer=timer,
                name='air_con_coef',
                phase=(AllPhase,),
                value=1.,
                atk_request=[BuffRequest_1])
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        if self.atk.atk_body.side == 1:
            air_con_flag = self.timer.air_con_flag
        else:
            air_con_flag = 6 - self.timer.air_con_flag
        return air_con_flag > 3


class Skill_111201_4(Skill):
    """制空权均势、优势和确保时增加舰载机15%伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='air_atk_buff',
                phase=(AllPhase,),
                value=0.15,
                bias_or_weight=2,
                atk_request=[BuffRequest_2]
            )
        ]


class BuffRequest_2(ATKRequest):
    def __bool__(self):
        if self.atk.atk_body.side == 1:
            air_con_flag = self.timer.air_con_flag
        else:
            air_con_flag = 6 - self.timer.air_con_flag
        return air_con_flag <= 3


skill = [Skill_111201_1, Skill_111201_2, Skill_111201_3, Skill_111201_4]
