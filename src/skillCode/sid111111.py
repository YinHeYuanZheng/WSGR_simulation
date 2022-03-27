# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 华盛顿-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""火控雷达(3级)：旗舰技，战斗中队伍中U国国籍船只的回避+10，炮击战阶段的火力+10，命中+10。
"""


class Skill_111111(Skill):
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = CountryTarget(side=1, country='U')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                value=10,
                phase=AllPhase,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                value=10,
                phase=ShellingPhase,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                value=10,
                phase=ShellingPhase,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


Skill = [Skill_111111]
