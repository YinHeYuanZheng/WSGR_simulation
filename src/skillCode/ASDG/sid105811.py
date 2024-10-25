# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 塞瓦斯托波尔-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队导巡、导战护甲穿透增加20%。
全队舰船索敌值增加4点、命中值增加12点，暴击率提高9%，S国舰船暴击率额外提高9%。"""


class Skill_105811_1(Skill):
    """全队导巡、导战护甲穿透增加20%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(KP, BBG))
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='pierce_coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]


class Skill_105811_2(PrepSkill):
    """全队舰船索敌值增加4点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            )
        ]


class Skill_105811_3(Skill):
    """全队舰船命中值增加12点，暴击率提高9%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.09,
                bias_or_weight=0
            )
        ]


class Skill_105811_4(Skill):
    """S国舰船暴击率额外提高9%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='S')
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.09,
                bias_or_weight=0
            )
        ]


name = '金雕展翅'
skill = [Skill_105811_1, Skill_105811_2, Skill_105811_3, Skill_105811_4]
