# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 彼得·施特拉塞尔-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *


class Skill_104261_1(Skill):
    """超重型航弹(3级)：增加自身20%暴击率。"""

    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [CoeffBuff(
            name='crit',
            phase=(AllPhase,),
            value=0.2,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        return True


class Skill_104261_2(Skill):
    """彼得·施特拉塞尔命中过的目标会降低10点闪避值与10点装甲值，
    如果是航母装母轻母单位还会再额外降低10点命中值（限炮击战阶段）。"""

    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)  # todo 被攻击目标
        self.buff = [StatusBuff(
            name='evasion',
            phase=(ShellingPhase, ),
            value=-10,
            bias_or_weight=0
        ), StatusBuff(
            name='armor',
            phase=(ShellingPhase, ),
            value=-10,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        return True


class Skill_104261_2(Skill):
    """如果是航母装母轻母单位还会再额外降低10点命中值（限炮击战阶段）。"""

    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = TypeTarget(side=0, shiptype=(CV, CVL, AV))  # todo 被攻击目标
        self.buff = [StatusBuff(
            name='accurace',
            phase=(ShellingPhase, ),
            value=-10,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        return True


class Request_1(Request):
    def __bool__(self):
        pass


skill = [Skill_104261_1]
