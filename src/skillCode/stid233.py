# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 后备弹

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身携带的弹药量增加20%"""


class Strategy_233(SelfStrategy):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='strategy_ammo',
                phase=AllPhase
            )
        ]
