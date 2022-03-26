# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 西弗吉尼亚-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""浴火重生(3级)：自身暴击率提升20%，自身每损失5点HP，在炮击战中便会增加10点固定伤害，最多增加100点固定伤害。
"""


class Skill_110231(Skill):
    """自身暴击率提升20%，自身每损失5点HP，在炮击战中便会增加10点固定伤害，最多增加100点固定伤害。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.20,
                bias_or_weight=0
            ), CoeffBuff_1(
                timer=timer
            )
        ]


class CoeffBuff_1(CoeffBuff):
    """自身每损失5点HP，在炮击战中便会增加10点固定伤害，最多增加100点固定伤害"""

    def __init__(self, timer):
        super().__init__(timer=timer,
                         name='extra_damage',
                         phase=ShellingPhase,
                         value=0,
                         bias_or_weight=0)

    def is_active(self, *args, **kwargs):
        value1 = 10 * ((self.master.status["total_health"] - self.master.status["total_health"]) // 5)
        self.value = value1 if value1 < 100 else 100
        return True
