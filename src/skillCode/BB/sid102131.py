# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 罗马-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_102131(Skill):
    """首轮炮击阶段，自身攻击时，敌人装甲降低40%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='ignore_armor',
                phase=FirstShellingPhase,
                value=-0.4,
                bias_or_weight=1
            )
        ]


name = '强装药主炮'
skill = [Skill_102131]
