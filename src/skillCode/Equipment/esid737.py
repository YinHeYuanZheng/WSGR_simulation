# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 特殊炮塔（T-34/76）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_737(EquipSkill):
    """增加X%攻击威力/攻击力"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=737,
                name='power_buff',
                phase=ShellingPhase,
                value=0.1,
                bias_or_weight=2
            )
        ]


skill = [Eskill_737]
