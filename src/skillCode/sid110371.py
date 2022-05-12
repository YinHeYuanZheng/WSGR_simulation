# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 布吕歇尔-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110371(Skill):
    """迷之自信(3级)：全阶段暴击率增加40%，被暴击率增加40%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.4,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='be_crit',
                phase=AllPhase,
                value=0.4,
                bias_or_weight=0
            )
        ]


skill = [Skill_110371]
