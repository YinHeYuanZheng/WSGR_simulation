# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# E国双联15英寸主炮（BM）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_605(EquipSkill):
    """重炮装备时增加10%护甲穿透和10%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if isinstance(master, BM):
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=3,
                    name='pierce_coef',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=605,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_605]
