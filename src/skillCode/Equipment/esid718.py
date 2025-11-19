# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 七联鱼雷发射器(93M3)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_718(EquipSkill):
    """J国舰船装备时增加5%攻击威力"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.status['country'] == 'J':
            self.buff.extend([
                EquipEffect(
                    timer=timer,
                    effect_type=718,
                    name='power_buff',
                    phase=AllPhase,
                    value=0.05,
                    bias_or_weight=2
                ),
            ])

skill = [Eskill_718]
