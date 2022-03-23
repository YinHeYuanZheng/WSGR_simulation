# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# L20-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
from src.wsgr.formulas import *
"""主炮群覆盖(3级)：单纵时增加自身10%暴击率。同航战时增加自身9点火力值；T优时增加20%暴击伤害。
"""


class Skill_104501_1(Skill):
    """单纵时增加自身10%暴击率"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return friend.form == 1


class Skill_104501_2(Skill):
    """同航战时增加自身9点火力值；"""

    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer,
                name='fire',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.timer.direction_flag == 2


class Skill_104501_3(Skill):
    """T优时增加20%暴击伤害。"""

    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.timer.direction_flag == 1


skill = [Skill_104501_1, Skill_104501_2, Skill_104501_3]
