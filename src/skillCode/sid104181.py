# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 阿金库尔-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""战列线(3级)：增加队伍中战列、战巡10点火力值，
单纵阵时增加己方全体12点火力值与10点命中值，
梯形阵时增加己方全体15%暴击率与7%被暴击率。
"""


class Skill_104181_1(Skill):
    """增加队伍中战列、战巡10点火力值，"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = TypeTarget(side=1, shiptype=(BB, BC))
        self.buff = [
            StatusBuff(
                timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_104181_2(Skill):
    """单纵阵时增加己方全体12点火力值与10点命中值，"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 1


class Skill_104181_3(Skill):
    """梯形阵时增加己方全体15%暴击率与7%被暴击率。"""

    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = Target(side=1)
        self.buff = [
            CoeffBuff(
                timer,
                name='crit',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer,
                name='be_crit',
                phase=AllPhase,
                value=0.07,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 4


skill = [Skill_104181_1, Skill_104181_2, Skill_104181_3]
