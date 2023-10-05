# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# AJ-2(空中加油系统)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""航空战阶段增加5%攻击威力；炮击战阶段增加20%攻击威力"""


class Eskill_657(EquipSkill):
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=657.1,
                name='power_buff',
                phase=AirPhase,
                value=0.05,
                bias_or_weight=2
            ),
            EquipEffect(
                timer=timer,
                effect_type=657.2,
                name='power_buff',
                phase=ShellingPhase,
                value=0.2,
                bias_or_weight=2
            ),
        ]


skill = [Eskill_657]
