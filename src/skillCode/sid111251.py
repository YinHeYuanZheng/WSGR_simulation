# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 埃罗芒什改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *


class Skill_110231_1(CommonSkill):
    """增加自身鱼雷机8点对潜值"""

    def __init__(self, master):
        super().__init__(master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=(DiveBomber,)
        )
        self.buff = [
            CommonBuff(
                name='antisub',
                phase=(AllPhase,),
                value=8,
                bias_or_weight=0
            )
        ]


class Skill_110231_2(CommonSkill):
    """增加自身轰炸机8点轰炸值"""

    def __init__(self, master):
        super().__init__(master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=(Bomber,)
        )
        self.buff = [
            CommonBuff(
                name='bomb',
                phase=(AllPhase,),
                value=8,
                bias_or_weight=0
            )
        ]


skill = [Skill_110231_1, Skill_110231_2]
