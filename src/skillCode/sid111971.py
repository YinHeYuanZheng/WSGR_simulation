# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# U-47 突袭帕斯卡湾

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身耐久 5 点，增加暴击几率 20%。"""


class Skill_111971_1(Skill):
    """增加自身耐久 5 点，增加暴击几率 20%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master, side=1)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='health',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.2,
                bias_or_weight=0
            )
        ]
skill = [Skill_111971_1,]
