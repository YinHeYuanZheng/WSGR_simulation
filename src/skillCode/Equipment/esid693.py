# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# KT-35发射器

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_693(EquipSkill):
    """塞瓦斯托波尔装备时提高10%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10581', '11581']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=693,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_693]
