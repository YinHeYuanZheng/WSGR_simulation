# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 约克公爵改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队C国、E国、F国、S国和U国舰船火力值和命中值增加20点、暴击伤害提高20%。
自身攻击敌方大型船时伤害提高30%。"""


class Skill_112052_1(Skill):
    """全队C国、E国、F国、S国和U国舰船火力值和命中值增加20点、暴击伤害提高20%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='CEFSU')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]


class Skill_112052_2(Skill):
    """自身攻击敌方大型船时伤害提高30%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=.3,
                atk_request=[ATKRequest_1]
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, LargeShip)


name = '骑士之矛'
skill = [Skill_112052_1, Skill_112052_2]
