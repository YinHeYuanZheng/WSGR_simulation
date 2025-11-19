# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 最终伤害

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_008(EquipSkill):
    """增加X%伤害"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=8,
                name='final_damage_buff',
                phase=AllPhase,
                value=self.value[0],
                bias_or_weight=2
            )
        ]


skill = [Eskill_008]
