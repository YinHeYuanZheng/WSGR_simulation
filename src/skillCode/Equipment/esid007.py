# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 命中率特效

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_007(EquipSkill):
    """增加X%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=7,
                name='hit_rate',
                phase=AllPhase,
                value=self.value[0],
                bias_or_weight=0
            )
        ]

skill = [Eskill_007]
