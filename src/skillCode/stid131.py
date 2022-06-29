# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 大角度

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import *

"""炮击战阶段受到炮击时，有15%概率免疫此攻击"""


class Strategy_131(SelfStrategy):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.stid = '131'
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='strategy_shield',
                phase=ShellingPhase,
                rate=0.15
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, NormalAtk)


skill = [Strategy_131]
