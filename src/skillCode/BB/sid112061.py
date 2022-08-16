# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 北卡罗来纳-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""灵活转换(形态一)(3级)：非中破、大破状态下，提升自身闪避值20点、装甲值15点，降低自身火力值7点；
中破状态下，自身火力不受战损影响
"""


class Skill_112061(Skill):
    """非中破、大破状态下，提升自身闪避值20点、装甲值15点，降低自身火力值7点；中破状态下，自身火力不受战损影响"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            ShiftBuff_1(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            ShiftBuff_1(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            ShiftBuff_1(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-7,
                bias_or_weight=0
            ),
            ShiftBuff_2(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase
            )
        ]


class ShiftBuff_1(StatusBuff):
    def is_active(self, *args, **kwargs):
        return self.master.damaged == 1


class ShiftBuff_2(SpecialBuff):
    def is_active(self, *args, **kwargs):
        return self.master.damaged == 2


skill = [Skill_112061]
