# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 日丹诺夫改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队S国护卫舰索敌值和命中值增加5点。
全队轻巡对空值和回避值增加30点。
自身为舰队旗舰时，全队轻巡攻击时有50%概率无视敌方装甲值。"""


class Skill_115161_1(PrepSkill):
    """全队S国护卫舰索敌值增加5点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[CountryTarget(side=1, country='S'),
                         TypeTarget(side=1, shiptype=CoverShip)]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


class Skill_115161_2(Skill):
    """全队S国护卫舰命中值增加5点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[CountryTarget(side=1, country='S'),
                         TypeTarget(side=1, shiptype=CoverShip)]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


class Skill_115161_3(Skill):
    """全队轻巡对空值和回避值增加30点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=CL)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            )
        ]


class Skill_115161_4(Skill):
    """自身为舰队旗舰时，全队轻巡攻击时有50%概率无视敌方装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=CL)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='ignore_armor',
                phase=AllPhase,
                value=-1,
                bias_or_weight=1,
                rate=0.5
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


name = '舰队指挥'
skill = [Skill_115161_1, Skill_115161_2, Skill_115161_3, Skill_115161_4]
