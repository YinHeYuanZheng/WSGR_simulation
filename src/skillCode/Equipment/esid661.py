# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 76A式

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

class Eskill_661(EquipSkill):
    """C国舰船装备时提高5%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.status['country'] == 'C':
            self.buff.extend([
                EquipEffect(
                    timer=timer,
                    effect_type=661,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                ),
            ])


skill = [Eskill_661]
