# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 照明弹校正

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""在夜战阶段，提高命中2/4/6/8点。"""


class Strategy_332(SelfStrategy):
    def __init__(self, timer, master, level=3):
        super().__init__(timer, master, level)
        value = [2, 4, 6, 8]
        self.stid = '332'
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=NightPhase,
                value=value[self.level],
                bias_or_weight=0
            )
        ]


skill = [Strategy_332]
