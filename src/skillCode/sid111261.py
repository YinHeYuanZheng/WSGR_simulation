# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 普林斯顿改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *


class Skill_111261_1(CommonSkill):
    """战斗机对空值+30%"""
    def __init__(self, master):
        super().__init__(master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=(Fighter,)
        )
        self.buff = [
            CommonBuff(
                name='antiair',
                phase=(AllPhase,),
                value=0.3,
                bias_or_weight=1
            )
        ]


class Skill_111261_2(Skill):
    """战斗中鱼雷机威力+15%"""

    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='air_dive_atk_buff',
                phase=(AllPhase,),
                value=0.15,
                bias_or_weight=2
            )
        ]


skill = [Skill_111261_1, Skill_111261_2]
