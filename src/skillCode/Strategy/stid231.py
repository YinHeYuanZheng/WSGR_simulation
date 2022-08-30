# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 交互射击

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import NormalAtk

"""炮击战阶段受到炮击后，有5%/10%/15%/20%概率进行一次反击。"""


class Strategy_231(SelfStrategy):
    def __init__(self, timer, master, level=3):
        super().__init__(timer, master, level)
        value = [0.05, 0.1, 0.15, 0.2]
        self.stid = '231'
        self.buff = [
            HitBack(
                timer=timer,
                name='strategy_hit_back',
                phase=ShellingPhase,
                exhaust=None,
                atk_request=[ATKRequest_1],
                rate=value[self.level]
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, NormalAtk)


skill = [Strategy_231]
