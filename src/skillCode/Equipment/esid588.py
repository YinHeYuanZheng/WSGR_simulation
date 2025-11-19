# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# TBD鱼雷机（VT-8）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_588(EquipSkill):
    """航空战阶段提高15%伤害和10%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=588.1,
                name='final_damage_buff',
                phase=AirPhase,
                value=0.15,
                bias_or_weight=2
            ),
            EquipEffect(
                timer=timer,
                effect_type=588.2,
                name='hit_rate',
                phase=AirPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]


skill = [Eskill_588]
