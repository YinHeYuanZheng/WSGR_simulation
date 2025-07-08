# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# MK7主炮（MK8）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_721(EquipSkill):
    """衣阿华级装备时增加10%攻击威力与10%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.status['tag'] == 'iowa':
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=721.1,
                    name='power_buff',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=2
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=721.2,
                    name='hit_rate',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                ),
            ]


skill = []
