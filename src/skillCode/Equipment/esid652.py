# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# A4D

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""埃塞克斯级航母装备时增加10%攻击力与15制空值"""


class Eskill_652(EquipSkill):
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.status['tag'] == 'essex':
            self.buff = [
                CoeffBuff(
                    timer=timer,
                    name='power_buff',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=2
                ),
                CoeffBuff(
                    timer=timer,
                    name='air_con_buff',
                    phase=AirPhase,
                    value=15,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_652]
