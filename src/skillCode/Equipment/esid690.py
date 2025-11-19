# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_690(EquipSkill):
    """中途岛装备时增加10%攻击威力"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10576', '11576']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=690,
                    name='power_buff',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=2
                )
            ]

skill = [Eskill_690]
