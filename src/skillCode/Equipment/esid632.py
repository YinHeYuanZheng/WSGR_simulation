# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 马舒卡防空系统

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""絮弗伦装备时提高10%回避率，降低敌方航空战阶段5%命中率"""


class Eskill_632_1(EquipSkill):
    """絮弗伦装备时提高10%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10552', '11552']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=632.1,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                )
            ]


class Eskill_632_2(EquipSkill):
    """降低敌方航空战阶段5%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = Target(side=0)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=632.2,
                name='hit_rate',
                phase=AirPhase,
                value=-0.05,
                bias_or_weight=0
            )
        ]


skill = [Eskill_632_1, Eskill_632_2]
