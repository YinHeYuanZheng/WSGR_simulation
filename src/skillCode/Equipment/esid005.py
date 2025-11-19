# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 高脚柜特效

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_005(EquipSkill):
    """装备时，增加X%开幕轰炸攻击力"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=5,
                name='air_bomb_atk_buff',
                phase=AirPhase,
                value=self.value[0],
                bias_or_weight=2
            )
        ]


skill = [Eskill_005]
