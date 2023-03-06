# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 开幕轰炸威力特效

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_630(EquipSkill):
    """装备时提高X%开幕轰炸攻击力"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=24,
                name='air_bomb_atk_buff',
                phase=AllPhase,
                value=self.value[0],
                bias_or_weight=2
            )
        ]


skill = [Eskill_630]
