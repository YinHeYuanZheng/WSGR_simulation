# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 潜载发射筒(033G)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_713(EquipSkill):
    """351装备时提高10%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10601', '11601']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=713,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_713]
