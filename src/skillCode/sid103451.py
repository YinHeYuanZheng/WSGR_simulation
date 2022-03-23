# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 威斯康星-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

"""高速特遣队(3级)：炮击战阶段,降低敌方高速舰（速度≥27）命中率6%。
威斯康星为旗舰时，本方战列、战巡、航战、重巡首轮炮击命中率增加9%，次轮炮击暴击率增加9%。
"""


class Skill_103451_1(Skill):
    """炮击战阶段,降低敌方高速舰（速度≥27）命中率6%。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = StatusTarget(side=0,
                                   status_name='speed',
                                   fun="ge",
                                   value=27)
        self.buff = [
            CoeffBuff(
                timer,
                name="hit_rate",
                phase=ShellingPhase,
                value=-0.06,
                bias_or_weight=0
            )
        ]


class Skill_103451_2(Skill):
    """威斯康星为旗舰时，本方战列、战巡、航战、重巡首轮炮击命中率增加9%，次轮炮击暴击率增加9%。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = TypeTarget(side=1,
                                 shiptype=(BB, BC, BBV, CA))
        self.buff = [
            CoeffBuff(
                timer,
                name="hit_rate",
                phase=FirstShellingPhase,
                value=0.09,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer,
                name="crit",
                phase=SecondShellingPhase,
                value=0.09,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


skill = [Skill_103451_1, Skill_103451_2]
