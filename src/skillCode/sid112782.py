# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 霍埃尔-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""大卫·塔菲3(3级)：增加自身回避、命中、幸运20点。
"""


class Skill_112782(CommonSkill):
    """增加自身回避、命中、幸运20点。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='luck',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


name = '大卫·塔菲3'
skill = [Skill_112782]
