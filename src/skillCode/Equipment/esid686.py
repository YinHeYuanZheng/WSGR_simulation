# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 天河攻击机（KI-148）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_686(EquipSkill):
    """增加25%护甲穿透（同类效果只生效一个）
    J国舰船装备时增加20%攻击威力"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=3,
                name='pierce_coef',
                phase=AllPhase,
                value=0.25,
                bias_or_weight=0
            )
        ]
        if master.status['country'] == 'J':
            self.buff.extend([
                EquipEffect(
                    timer=timer,
                    effect_type=686,
                    name='power_buff',
                    phase=AllPhase,
                    value=0.2,
                    bias_or_weight=2
                )
            ])

skill = [Eskill_686]
