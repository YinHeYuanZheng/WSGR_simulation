# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# M1导弹

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_620(EquipSkill):
    """装备时提高10%伤害"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=620,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=2
            )
        ]


skill = [Eskill_620]
