# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 烈风改J特效

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_012(EquipSkill):
    """降低敌方航空战阶段X%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = Target(side=0)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=12,
                name='hit_rate',
                phase=AirPhase,
                value=self.value[0],
                bias_or_weight=0
            )
        ]


skill = [Eskill_012]
