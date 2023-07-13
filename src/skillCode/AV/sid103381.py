# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 天鹰-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""地中海护卫(3级)：炮击战时增加自身暴击率12%，降低对方所有航母及轻母炮击战时的命中值12点。
"""


class Skill_103381_1(Skill):
    """炮击战时增加自身暴击率12%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=ShellingPhase,
                value=0.12,
                bias_or_weight=0
            )
        ]


class Skill_103381_2(Skill):
    """降低对方所有航母及轻母炮击战时的命中值12点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(CV, CVL))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=ShellingPhase,
                value=-12,
                bias_or_weight=0
            )
        ]


name = '地中海护卫'
skill = [Skill_103381_1, Skill_103381_2]
