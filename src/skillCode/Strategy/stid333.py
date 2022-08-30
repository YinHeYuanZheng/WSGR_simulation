# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 对空预警

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""航空战阶段受到轰炸时，有5%/10%/15%/20%的概率免疫该次攻击。"""


class Strategy_333(SelfStrategy):
    def __init__(self, timer, master, level=3):
        super().__init__(timer, master, level)
        value = [0.05, 0.1, 0.15, 0.2]
        self.stid = '333'
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='strategy_shield',
                phase=AirPhase,
                rate=value[self.level]
            )
        ]


skill = [Strategy_333]
