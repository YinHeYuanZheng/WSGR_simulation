# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 7231发射系统（ZL-1）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""鹰潭装备时提高10%回避率，降低敌方航空战阶段5%命中率"""


class Eskill_671_1(EquipSkill):
    """鹰潭装备时提高10%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10287', '11287']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=671.1,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                )
            ]


class Eskill_671_2(EquipSkill):
    """鹰潭装备时降低敌方航空战阶段5%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = Target(side=0)
        self.buff = []
        if master.cid in ['10287', '11287']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=671.2,
                    name='hit_rate',
                    phase=AirPhase,
                    value=-0.05,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_671_1, Eskill_671_2]
