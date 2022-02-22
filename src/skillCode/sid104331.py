# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 提康德罗加-1
from ..wsgr.formulas import AirAtk
from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *


class Skill_104331_1(Skill):
    """制空权(3级)：自身受到航母单位攻击时降低20%的伤害（限开幕与炮击战阶段）。
    自身和其上方最近的一艘航母，装母，轻母单位在制空权均势，优势，确保时舰载机伤害增加10%。
"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [FinalDamageBuff(
            name='final_damage_debuff',
            phase=(AirPhase, ShellingPhase),
            value=-0.2,
            atk_request=[BuffRequest_1],
            bias_or_weight=2
        )]

    def is_active(self, friend, enemy):
        return True


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, AirAtk)


class Skill_104331_2(Skill):
    """自身和其上方最近的一艘航母，装母，轻母单位在制空权均势，优势，确保时舰载机伤害增加10%。"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = NearestLocTarget(side=1,
                                       master=master,
                                       radius=1,
                                       direction='up',
                                       master_include=True,
                                       expand=True)
        self.buff = [CoeffBuff(
            name='air_atk_buff',
            phase=(AirPhase, ),
            value=0.1,
            bias_or_weight=2
        )]

    def is_active(self, friend, enemy):
        return True


class Request_1(Request):
    # todo
    def __bool__(self):
        pass


skill = [Skill_104331_1]
