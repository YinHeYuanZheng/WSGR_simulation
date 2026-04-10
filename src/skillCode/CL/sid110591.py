# -*- coding: utf-8 -*-
# Author:银河远征
# env:py38
# 海伦娜改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""情报分析(3级)：全队舰船索敌值和命中值增加10点，暴击率提高10%。迂回时最终迂回率提高45%。"""


class Skill_110591_1(PrepSkill):
    """己方所有舰船索敌+10"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_110591_2(Skill):
    """己方所有舰船命中+10，暴击率+10%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]


class Skill_110591_3(CommonSkill):
    """迂回时最终迂回率提高45%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            RoundaboutBuff(
                timer=timer,
                phase=AllPhase,
                value=0.45,
                bias_or_weight=0
            )
        ]


name = '情报分析'
skill = [Skill_110591_1, Skill_110591_2, Skill_110591_3]
