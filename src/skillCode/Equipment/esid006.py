# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 鱼雷机威力

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_006(EquipSkill):
    """装备时，增加X%开幕鱼雷机威力"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=6,
                name='air_dive_atk_buff',
                phase=AirPhase,
                value=self.value[0],
                bias_or_weight=2
            )
        ]


skill = [Eskill_006]
