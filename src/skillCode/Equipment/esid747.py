# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 五联鱼雷发射器（53-65）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_747(EquipSkill):
    """S国舰船装备时增加20%暴击率和10%攻击威力"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.status['country'] == 'S':
            self.buff.extend([
                EquipEffect(
                    timer=timer,
                    effect_type=747.1,
                    name='crit',
                    phase=AllPhase,
                    value=0.2,
                    bias_or_weight=0
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=747.2,
                    name='power_buff',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=2
                ),
            ])


skill = [Eskill_747]
