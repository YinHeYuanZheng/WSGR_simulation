# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 远程对空警戒雷达

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_018(EquipSkill):
    """航空战阶段增加X1%回避率，炮击战阶段增加X2%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=18.1,
                name='miss_rate',
                phase=AirPhase,
                value=self.value[0],
                bias_or_weight=0
            ),
            EquipEffect(
                timer=timer,
                effect_type=18.2,
                name='miss_rate',
                phase=ShellingPhase,
                value=self.value[1],
                bias_or_weight=0
            )
        ]


skill = [Eskill_018]
