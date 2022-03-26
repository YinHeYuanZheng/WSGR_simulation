# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 北卡罗来纳-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""灵活转换(形态一)(3级)：非中破、大破状态下，提升自身闪避值20点、装甲值15点，降低自身火力值7点；中破状态下，自身火力不受战损影响
"""


class Skill_112061(Skill):
    """非中破、大破状态下，提升自身闪避值20点、装甲值15点，降低自身火力值7点；中破状态下，自身火力不受战损影响"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff_1(
                timer=timer,
                name='evasion',
                value=20,
            ), StatusBuff_1(
                timer=timer,
                name='armor',
                value=15,
            ), StatusBuff_1(
                timer=timer,
                name='fire',
                value=-7,
            ), SpecialBuff_1(
                timer=timer
            )
        ]


class StatusBuff_1(StatusBuff):
    def __init__(self, timer, name, value):
        super().__init__(timer=timer,
                         name=name,
                         phase=AllPhase,
                         value=value,
                         bias_or_weight=0)

    def is_active(self, *args, **kwargs):
        return self.master.damaged < 2


class SpecialBuff_1(SpecialBuff):
    def __init__(self, timer):
        super().__init__(timer=timer,
                         name='ignore_damaged',
                         phase=AllPhase
                         )

    def is_active(self, *args, **kwargs):
        return self.master.damaged == 2


Skill = [Skill_112061]
