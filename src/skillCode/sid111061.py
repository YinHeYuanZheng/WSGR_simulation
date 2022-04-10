# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 田纳西-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""	T优时，自身基础火力值提升40%，基础命中值提升40%。"""


class Skill_111061(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=0.4,
                bias_or_weight=1
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=0.4,
                bias_or_weight=1
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_dir_flag() == 1


skill = [Skill_111061]
