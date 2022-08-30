# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 威尔士亲王-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""队伍中所有U国和E国舰船命中值增加7，如果威尔士亲王处于旗舰位置，则自身获得2倍buff效果。"""


class Skill_110101_1(Skill):
    """队伍中所有U国和E国舰船命中值增加7"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='UE')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=7,
                bias_or_weight=0
            )
        ]


class Skill_110101_2(Skill):
    """如果威尔士亲王处于旗舰位置，则自身获得2倍buff效果"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=7,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


skill = [Skill_110101_1, Skill_110101_2]
