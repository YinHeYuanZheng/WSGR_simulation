# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 狮-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
"""根据总出征次数(上限30000次)增加自身火力最多12点，且增加自身暴击率最多12%"""


class Skill_111001(Skill):
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.12,
                bias_or_weight=0
            )
        ]


skill = [Skill_111001]
