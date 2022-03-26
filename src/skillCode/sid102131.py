# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 罗马-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_102131(Skill):
    """首轮炮击阶段，自身攻击时，敌人装甲降低40%。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='ignore_armor',
                value=-0.4,
                phase=FirstShellingPhase,
                bias_or_weight=1
            )
        ]


skill = [Skill_102131]
