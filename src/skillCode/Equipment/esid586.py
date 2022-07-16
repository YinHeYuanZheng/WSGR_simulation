# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 潜载火箭炮特效

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_586(EquipSkill):
    """先制鱼雷和鱼雷战阶段提高10%伤害和10%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=586.1,
                name='final_damage_buff',
                phase=TorpedoPhase,
                value=0.1,
                bias_or_weight=2
            ),
            EquipEffect(
                timer=timer,
                effect_type=586.2,
                name='hit_rate',
                phase=TorpedoPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]


skill = [Eskill_586]
