# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 约克城改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
"""萨奇剪(3级)：提升自身10点火力值和航空战25点制空值；制空权劣势和丧失时不降低舰载机伤害，制空权均势、优势和确保时增加舰载机15%伤害。
"""


class Skill_111201(Skill):
    def __init__(self, master):
        # 提升自身10点火力值和航空战25点制空值
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                name='fire',
                phase=('AllPhase', ),
                value=10,
                bias_or_weight=0
            ), CoeffBuff(
                name='air_con_buff',
                phase=('AirPhase', ),
                value=25,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return True


class Skill_111201_1(Skill):
    def __init__(self, master):
        # todo 制空权劣势和丧失时不降低舰载机伤害，
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.request = [Request_1]
        self.buff = [

        ]

    def is_active(self, friend, enemy):
        return bool(self.request[0](self.master, friend, enemy))


class Request_1(Request):
    def __bool__(self):
        return self.timer.air_con_flag > 3


class Skill_111201_2(Skill):
    def __init__(self, master):
        # 制空权均势、优势和确保时增加舰载机15%伤害。
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.request = [Request_2]
        self.buff = [
            CoeffBuff(
                name='air_atk_buff',
                phase=('AllPhase', ),
                value=0.15,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return bool(self.request[0](self.master, friend, enemy))


class Request_2(Request):
    def __bool__(self):
        return self.timer.air_con_flag <= 3



skill = [Skill_111201]