# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# （三式）六联53厘米鱼雷发射器

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_711(EquipSkill):
    """驱逐装备时增加15%攻击威力"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if isinstance(master, DD):
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=711,
                    name='power_buff',
                    phase=AllPhase,
                    value=0.15,
                    bias_or_weight=2
                ),
            ]

skill = [Eskill_711]
