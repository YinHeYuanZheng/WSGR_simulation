# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 乌戈里尼·维瓦尔迪

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""奋战到底(3级)：自身鱼雷值+20，战斗中不受中破以及大破带来的属性减益效果。
"""


class Skill_111881_1(CommonSkill):
    """自身鱼雷值+20"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


class Skill_111881_2(Skill):
    """战斗中不受中破以及大破带来的属性减益效果"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase,
            )
        ]


name = '奋战到底'
skill = [Skill_111881_1, Skill_111881_2]
