# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 里昂-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
from src.wsgr.formulas import *
"""侧舷火力(3级)：增加自身15点火力值，降低自身3点命中值。
T优时，炮击战阶段必暴击；
T劣时，增加自身35点火力值，降低自身4点命中值。
"""


class Skill_104811_1(CommonSkill):
    """增加自身15点火力值，降低自身3点命中值。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            CommonBuff(
                timer,
                name='Accuracy',
                phase=AllPhase,
                value=-3,
                bias_or_weight=0
            )
        ]


class Skill_104811_2(Skill):
    """T优时，炮击战阶段必暴击；"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer,
                name='must_crit',
                phase=ShellingPhase,
            )
        ]

    def is_active(self, friend, enemy):
        return self.timer.direction_flag == 1


class Skill_104811_3(Skill):
    """T劣时，增加自身35点火力值，降低自身4点命中值。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer,
                name='fire',
                phase=AllPhase,
                value=35,
                bias_or_weight=0
            ),
            CommonBuff(
                timer,
                name='Accuracy',
                phase=AllPhase,
                value=-4,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.timer.direction_flag == 4


skill = [Skill_104811_1, Skill_104811_2, Skill_104811_3]
