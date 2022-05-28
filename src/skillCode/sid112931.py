# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# U-96

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身 30 点回避值和 30% 被攻击概率。自身有攻击轻巡、驱逐"""


class Skill_112931_1(Skill):
    """增加自身 30 点回避值和 30% 被攻击概率。自身有攻击轻巡、驱逐"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master, side=1)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=30,
                bias_or_weight=0,
            ),
            MagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=.3,
            ),
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=AllPhase,
                target=TypeTarget(side=0, shiptype=(DD, CL)),
                ordered=False,
            )
        ]

skill = [Skill_112931_1,]

