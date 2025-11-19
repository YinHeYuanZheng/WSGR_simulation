# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 炮塔后备弹

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身携带的弹药量增加10%/10%/10%/20%。"""


class Strategy_233(SelfStrategy):
    def __init__(self, timer, master, level=3):
        super().__init__(timer, master, level)
        value = [1, 1, 1, 2]
        self.stid = '233'
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='strategy_ammo',
                phase=AllPhase,
                value=value[self.level],
                bias_or_weight=0
            )
        ]


skill = [Strategy_233]
