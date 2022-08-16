# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 大淀改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加全队舰船5点索敌值和10点命中值。增加我方小型船15%暴击率。"""


class Skill_112481_1(PrepSkill):
    """增加全队舰船5点索敌值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=(AllPhase,),
                value=5,
                bias_or_weight=0
            )
        ]


class Skill_112481_2(Skill):
    """增加全队舰船10点命中值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=(AllPhase,),
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_112481_3(Skill):
    """增加我方小型船15%暴击率。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(SmallShip,))
        self.buff = [
            CoeffBuff(
                timer,
                name='crit',
                phase=(AllPhase,),
                value=0.15,
                bias_or_weight=0
            )
        ]


# 该舰船可以使用航母飞机类装备

name = '航空支援'
skill = [Skill_112481_1, Skill_112481_2, Skill_112481_3]
