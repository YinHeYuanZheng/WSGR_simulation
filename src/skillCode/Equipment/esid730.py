# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 海鹰导弹发射器（352）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_730(EquipSkill):
    """南京装备时提高15%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10617', '11617']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=730,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.15,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_730]
