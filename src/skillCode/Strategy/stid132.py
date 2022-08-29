# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 雁行雷击

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""闭幕雷击时，自身有5%/10%/15%/20%的概率多发射一枚鱼雷。"""


class Strategy_132(SelfStrategy):
    def __init__(self, timer, master, level=3):
        super().__init__(timer, master, level)
        value = [0.05, 0.1, 0.15, 0.2]
        self.stid = '132'
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='strategy_multi_torpedo',
                phase=SecondTorpedoPhase,
                rate=value[self.level]
            )
        ]


skill = [Strategy_132]
