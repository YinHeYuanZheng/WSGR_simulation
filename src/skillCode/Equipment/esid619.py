# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# AM-1拳击手（HVAR）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_619(EquipSkill):
    """增加15%暴击率和5%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=619.1,
                name='crit',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0
            ),
            EquipEffect(
                timer=timer,
                effect_type=619.2,
                name='hit_rate',
                phase=AllPhase,
                value=0.05,
                bias_or_weight=0
            )
        ]


skill = [Eskill_619]
