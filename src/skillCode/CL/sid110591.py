# -*- coding: utf-8 -*-
# Author:银河远征
# env:py38
# 海伦娜改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""情报分析(3级)：己方所有舰船索敌+5，命中+5。"""


class Skill_110591_1(PrepSkill):
    """己方所有舰船索敌+5"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


class Skill_110591_2(Skill):
    """己方所有舰船命中+5"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


name = '情报分析'
skill = [Skill_110591_1, Skill_110591_2]
