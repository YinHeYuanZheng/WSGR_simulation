# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 约克公爵-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *

"""骑士之誓(3级)：队伍中每有一艘非E国的船只都会增加自身命中、回避、火力3点。
"""


class Skill_102051(Skill):
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        ENumber = StatusTarget(side=1,
                               status_name="country",
                               fun="eq",
                               value='E').get_target(master.friend, master.enemy)
        SkillValue = (6 - len(ENumber)) * 3
        self.buff = [
            StatusBuff(
                timer,
                name="fire",
                phase=AllPhase,
                value=SkillValue,
                bias_or_weight=0
            ),
            StatusBuff(
                timer,
                name="evasion",
                phase=AllPhase,
                value=SkillValue,
                bias_or_weight=0
            ),
            StatusBuff(
                timer,
                name="accuracy",
                phase=AllPhase,
                value=SkillValue,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return True


skill = [Skill_102051]
