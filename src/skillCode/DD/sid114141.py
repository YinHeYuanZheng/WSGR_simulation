# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 凯利改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队E国护卫舰攻击时有30%概率无视敌方装甲值。自身为旗舰时，全队E国小型船造成的伤害提升30%。"""


class Skill_114141_1(Skill):
    """全队E国护卫舰攻击时有30%概率无视敌方装甲值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                CountryTarget(side=1, country='E'),
                TypeTarget(side=1, shiptype=CoverShip),
            ]
        )
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='ignore_armor',
                phase=AllPhase,
                value=-1,
                bias_or_weight=1,
                rate=0.3
            )
        ]


class Skill_114141_2(Skill):
    """自身为旗舰时，全队E国小型船造成的伤害提升30%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                CountryTarget(side=1, country='E'),
                TypeTarget(side=1, shiptype=SmallShip),
            ]
        )
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.3
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1



name = '战歌'
skill = [Skill_114141_1, Skill_114141_2]
