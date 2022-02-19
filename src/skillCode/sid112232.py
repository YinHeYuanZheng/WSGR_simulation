# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 信浓改-2

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_112232_1(Skill):
    def __init__(self, master):
        """航空战阶段，提升自身前方三个位置的航母、装母、轻母20%的伤害。"""
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)  # todo 自身前三个航系
        self.buff = [
            CoeffBuff(
                name='',  # todo 航空终伤倍率
                phase=(AirPhase, ),
                value=0.2,
                bias_or_weight=2
            )
        ]


class Skill_112232_2(Skill):
    def __init__(self, master):
        """当队伍中除了自己，不含有其他航母、轻母、装母时，增加自身装甲值35点与索敌值25点，"""
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.request = [Request_1]
        self.buff = [
            StatusBuff(
                name='armor',
                phase=(AllPhase, ),
                value=35,
                bias_or_weight=0
            ), StatusBuff(
                name='recon',
                phase=(AllPhase, ),
                value=25,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return bool(self.request[0](self.master, friend, enemy))


class Request_1(Request):
    def __bool__(self):
        return len(TypeTarget(
            side=1,
            shiptype=(CV, CVL, AV)
        ).get_target(self.friend, self.enemy)) == 1


class Skill_112232_3(Skill):
    def __init__(self, master):
        """炮击战阶段，自身被攻击概率增加35%"""
        # todo 嘲讽
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [

        ]


skill = [Skill_112232_1, Skill_112232_2, Skill_112232_3]
