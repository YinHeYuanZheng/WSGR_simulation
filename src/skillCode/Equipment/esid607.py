# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# CM.170

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_607(EquipSkill):
    """战斗结束获得经验增加10%(装备之间不叠加)；航空战阶段提高10%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=607,
                name='hit_rate',
                phase=AirPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]


skill = [Eskill_607]
