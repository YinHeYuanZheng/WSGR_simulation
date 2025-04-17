# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 351-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队小型船索敌值增加9点，护甲穿透增加15%，回避率提高10%。
自身攻击时无视目标装甲值。"""


class Skill_106011_1(PrepSkill):
    """全队小型船索敌值增加9点，"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=SmallShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=9,
                bias_or_weight=0,
            ),
        ]


class Skill_106011_2(Skill):
    """全队小型船护甲穿透增加15%，回避率提高10%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=SmallShip)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='pierce_coef',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='miss_rate',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]


class Skill_106011_3(PrepSkill):
    """自身攻击时无视目标装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='ignore_armor',
                phase=AllPhase,
                value=-1,
                bias_or_weight=1
            )
        ]


name = '大洋鹰击'
skill = [Skill_106011_1, Skill_106011_2, Skill_106011_3]