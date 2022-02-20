# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 大淀改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_112481_1(CommonSkill):
    """增加全队舰船5点索敌值和10点命中值。"""

    def __init__(self, master):
        super().__init__(master)
        self.target = Target(side=1)
        self.buff = [
            CommonBuff(
                name='recon',
                phase=(AllPhase,),
                value=5,
                bias_or_weight=0
            ), CommonBuff(
                name='accuracy',
                phase=(AllPhase,),
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_112481_2(Skill):
    """增加我方小型船15%暴击率。"""

    def __init__(self, master):
        super().__init__(master)
        self.target = TypeTarget(side=1, shiptype=(SmallShip,))
        self.buff = [
            CoeffBuff(
                name='crit',
                phase=(AllPhase,),
                value=0.15,
                bias_or_weight=0
            )
        ]


# 该舰船可以使用航母飞机类装备

skill = [Skill_112481_1, Skill_112481_2]
