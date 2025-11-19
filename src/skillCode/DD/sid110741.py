# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# Z1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""己方所有Z系列驱逐的攻击威力提升 11%。"""


class Skill_110741_1(Skill):
    """己方所有Z系列驱逐的攻击威力提升 11%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='z-ship')
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='power_buff',
                phase=AllPhase,
                value=0.11,
                bias_or_weight=2
            )
        ]


name = 'Z驱领舰'
skill = [Skill_110741_1]
