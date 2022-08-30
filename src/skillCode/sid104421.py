# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 里昂-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""侧舷火力(3级)：增加自身15点火力值，降低自身3点命中值。
T优时，炮击战阶段必暴击；
T劣时，增加自身35点火力值，降低自身4点命中值。
"""


class Skill_104421_1(CommonSkill):
    """增加自身15点火力值，降低自身3点命中值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-3,
                bias_or_weight=0
            )
        ]


class Skill_104421_2(Skill):
    """T优时，炮击战阶段必暴击；"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='must_crit',
                phase=ShellingPhase,
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_dir_flag() == 1


class Skill_104421_3(Skill):
    """T劣时，增加自身35点火力值，降低自身4点命中值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=35,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-4,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_dir_flag() == 4


skill = [Skill_104421_1, Skill_104421_2, Skill_104421_3]
