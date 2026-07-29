# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-3封锁战况(削弱前)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_080301_1(PrepSkill):
    """敌方重巡、轻巡的攻击必定命中"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=0, shiptype=(CA, CL))
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='must_hit',
                phase=AllPhase
            )
        ]


class NormalMap_080301_2(PrepSkill):
    """敌方驱逐可以进行开幕雷击"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=0, shiptype=DD)
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=FirstTorpedoPhase
            )
        ]


class NormalMap_080301_3(PrepSkill):
    """敌方在航空战阶段，伤害提高50%，受到伤害降低50%"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = Target(side=0)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AirPhase,
                value=0.5
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AirPhase,
                value=-0.5
            ),
        ]


name = '8-3封锁战况(削弱前)'
effect = '敌方重巡、轻巡的攻击必定命中；敌方驱逐可以进行开幕雷击；敌方在航空战阶段，伤害提高50%，受到伤害降低50%。'
skill = [NormalMap_080301_1, NormalMap_080301_2, NormalMap_080301_3]
