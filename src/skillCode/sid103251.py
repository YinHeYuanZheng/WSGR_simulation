# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 列克星敦(cv-16)-1
import random

from ..wsgr.formulas import *
from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_103251_1(Skill):
    """增加自身所携带轰炸机15%的威力"""
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='air_bomb_atk_buff',
                phase=(AllPhase, ),
                value=0.15,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        return True


class Skill_103251_2(Skill):
    """受到航空攻击时有25%概率免疫该次伤害"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = []  # todo 免疫伤害

    def is_active(self, friend, enemy):
        return bool()


class Request_1(ATKRequest):
    def __bool__(self):
        if isinstance(self.atk, (AirAtk,)) and True:  # 检测攻击对象是否为自己
            if random.randam < 0.25:
                return True
            else:
                return False


skill = [Skill_103251_1, Skill_103251_2]
