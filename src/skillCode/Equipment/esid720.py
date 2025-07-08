# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# SET-53鱼雷

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_720(EquipSkill):
    """增加30%护甲穿透(同类弹药效果只生效一个)，S国舰船装备时提高5%攻击威力与5%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=3,
                name='pierce_coef',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0
            )
        ]
        if master.status['country'] == 'S':
            self.buff.extend([
                EquipEffect(
                    timer=timer,
                    effect_type=712.1,
                    name='power_buff',
                    phase=AllPhase,
                    value=0.05,
                    bias_or_weight=2
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=712.2,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.05,
                    bias_or_weight=0
                ),
            ])


skill = []
