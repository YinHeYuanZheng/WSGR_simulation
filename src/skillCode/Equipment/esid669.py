# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# S-2反潜机

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_669(EquipSkill):
    """增加5%命中率，先制反潜阶段额外增加5%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=669.1,
                name='hit_rate',
                phase=AllPhase,
                value=.05,
                bias_or_weight=0
            ),
            EquipEffect(
                timer=timer,
                effect_type=669.2,
                name='hit_rate',
                phase=AntiSubPhase,
                value=.05,
                bias_or_weight=0
            ),
        ]


skill = [Eskill_669]
