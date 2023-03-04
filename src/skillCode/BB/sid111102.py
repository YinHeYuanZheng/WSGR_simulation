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
            ),
            ExtraDamage(
                timer=timer,
                name='extra_damage',
                phase=ShellingPhase,
                value=0,
                bias_or_weight=0
            )
        ]


class ExtraDamage(CoeffBuff):
    """自身每损失5点HP，在炮击战中便会增加10点固定伤害，最多增加100点固定伤害"""
    def is_active(self, *args, **kwargs):
        extra_damage = (self.master.status['standard_health'] -
                        self.master.status['health'])\
                       // 5 * 10
        self.value = min(100, extra_damage)
        return isinstance(self.timer.phase, self.phase)


name = '浴火重生'
skill = [Skill_110231]
