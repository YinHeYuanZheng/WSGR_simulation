# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# （CLT）四联鱼雷发射器（零式）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_704(EquipSkill):
    """雷巡装备时增加15%伤害和5%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if isinstance(master, CLT):
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=704.1,
                    name='final_damage_buff',
                    phase=AllPhase,
                    value=0.15,
                    bias_or_weight=2
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=704.2,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.05,
                    bias_or_weight=0
                ),
            ]


skill = [Eskill_704]
