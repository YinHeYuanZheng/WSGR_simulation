# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# F2G超级海盗（小提姆）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_630(EquipSkill):
    """装备时提高15%开幕轰炸攻击力"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=630,
                name='air_bomb_atk_buff',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=2
            )
        ]


skill = [Eskill_630]
