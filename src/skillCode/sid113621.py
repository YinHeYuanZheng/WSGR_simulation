# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 星座-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""特遣先锋：提升己方全队索敌 3 点，增加己方大型船闪避值 9 点，自身优先攻击排在前方的敌方大型船"""


class Skill_113621_1(PrepSkill):
    """提升己方全队索敌 3 点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=3,
                bias_or_weight=0,
            ),
        ]


class Skill_113621_2(Skill):
    """增加己方大型船闪避值 9 点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=LargeShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]


class Skill_113621_3(Skill):
    """自身优先攻击排在前方的敌方大型船"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=AllPhase,
                target=TypeTarget(side=0, shiptype=LargeShip),
                ordered=True
            )
        ]


skill = [Skill_113621_1, Skill_113621_2, Skill_113621_3]
