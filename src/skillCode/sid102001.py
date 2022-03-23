# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 兴登堡-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *


class Skill_102001(Skill):
    """当自身不处于中破、大破状态时，炮击战自身攻击时降低敌方装甲15%，并附带固定伤害20点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer,
                name="ignore_armor",
                phase=ShellingPhase,
                value=0.15,
                bias_or_weight=1
            ),
            CoeffBuff(
                timer,
                name="extra_damage",
                phase=ShellingPhase,
                value=20,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.damaged == 1


skill = [Skill_102001]
