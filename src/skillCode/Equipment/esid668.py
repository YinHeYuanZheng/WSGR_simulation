# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 四联533毫米鱼雷（ur高速）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_668(EquipSkill):
    """鱼雷战和夜战阶段提高10%伤害"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=668,
                name='final_damage_buff',
                phase=(SecondTorpedoPhase, NightPhase),
                value=0.15,
                bias_or_weight=2
            )
        ]


skill = [Eskill_668]
