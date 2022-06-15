# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 三坐标搜索雷达

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_022(EquipSkill):
    """航空战阶段增加X%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=22,
                name='miss_rate',
                phase=AirPhase,
                value=self.value[0],
                bias_or_weight=0
            )
        ]


skill = [Eskill_022]
