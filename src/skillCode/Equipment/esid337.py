# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 空射火箭弹

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_337(EquipSkill):
    """装备时，增加5%开幕轰炸攻击力，炮击战阶段增加5%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=337.1,
                name='air_atk_buff',
                phase=AirPhase,
                value=0.05,
                bias_or_weight=2
            ),
            EquipEffect(
                timer=timer,
                effect_type=337.2,
                name='hit_rate',
                phase=ShellingPhase,
                value=0.05,
                bias_or_weight=0
            )
        ]


skill = [Eskill_337]
