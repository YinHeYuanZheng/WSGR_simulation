# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 征服者-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""新锐战舰(3级)：提高全队9点命中值、降低自身3点回避值；
单纵时提高自身12点火力值、10点命中值；
梯形时提高全队9%暴击率；
复纵时提高全队9点回避值。
"""


class Skill_104541_1(Skill):
    """提高全队9点命中值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]


class Skill_104541_2(Skill):
    """降低自身3点回避值；"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-3,
                bias_or_weight=0
            )
        ]


class Skill_104541_3(Skill):
    """单纵时提高自身12点火力值、10点命中值；"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 1


class Skill_104541_4(Skill):
    """梯形时提高全队9%暴击率；"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.09,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 4


class Skill_104541_5(Skill):
    """复纵时提高全队9点回避值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 2


skill = [Skill_104541_1, Skill_104541_2, Skill_104541_3, Skill_104541_4, Skill_104541_5]
