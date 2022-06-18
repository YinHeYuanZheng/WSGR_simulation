# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 忠武

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""新装上阵(3级)：旗舰为航母、装母、战列或战巡时增加自身火力值9点和对空值12点；
旗舰不为航母、装母、战列或战巡时增加自身回避值12点和鱼雷值15点。
"""


class Skill_113421(Skill):
    """旗舰为航母、装母、战列或战巡时增加自身火力值9点和对空值12点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return isinstance(friend.ship[0], (CV, AV, BB, BC))


class Skill_113421_2(Skill):
    """旗舰不为航母、装母、战列或战巡时增加自身回避值12点和鱼雷值15点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return not isinstance(friend.ship[0], (CV, AV, BB, BC))


name = '新装上阵'
skill = [Skill_113421, Skill_113421_2]
