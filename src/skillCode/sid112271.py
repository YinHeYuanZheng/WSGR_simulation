# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 飞鹰改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
"""特设空母(3级)：炮击战阶段造成的最终伤害增加30%。
"""

class Skill_112271(Skill):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='',  # todo 终伤倍率
                phase=(AllPhase, ),  # todo 应为炮击阶段
                value=0.3,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        return True


skill = [Skill_112271]
