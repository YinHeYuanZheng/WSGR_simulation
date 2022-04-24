# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 大凤改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_111171_1(Skill):
    """全阶段降低敌方旗舰40点火力值和40点命中值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=0, loc=[1])
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=(AllPhase,),
                value=-40,
                bias_or_weight=0),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=(AllPhase,),
                value=-40,
                bias_or_weight=0)
        ]


class Skill_111171_2(Skill):
    """降低敌方主力舰20点火力值和20点装甲值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(MainShip,))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=(AllPhase,),
                value=-20,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=(AllPhase,),
                value=-20,
                bias_or_weight=0
            )
        ]


class Skill_111171_3(Skill):
    """降低敌方护卫舰15点闪避值和20点对空值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(CoverShip,))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=(AllPhase,),
                value=-15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=(AllPhase,),
                value=-20,
                bias_or_weight=0
            )
            ]


skill = [Skill_111171_1, Skill_111171_2, Skill_111171_3]
