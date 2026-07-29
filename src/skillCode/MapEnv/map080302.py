# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-3封锁战况(削弱后)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_080302_1(PrepSkill):
    """敌方航母、轻母、驱逐射程提高为长"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=0, shiptype=(CV, CVL, DD))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            )
        ]


class NormalMap_080302_2(PrepSkill):
    """敌方航母、轻母、装母可以参加夜战"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=0, shiptype=(CV, CVL, AV))
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=NightPhase
            )
        ]


class NormalMap_080302_3(PrepSkill):
    """敌方在炮击战阶段，伤害提高20%，受到伤害降低30%"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = Target(side=0)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.2
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=ShellingPhase,
                value=-0.3
            ),
        ]


name = '8-3封锁战况(削弱后)'
effect = '敌方航母、轻母、驱逐射程提高为长；敌方航母、轻母、装母可以参加夜战；敌方在炮击战阶段，伤害提高20%，受到伤害降低30%。'
skill = [NormalMap_080302_1, NormalMap_080302_2, NormalMap_080302_3]
