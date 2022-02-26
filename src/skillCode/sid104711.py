# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 欧罗巴-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
"""增加自身护甲穿透30%，根据总出征数(上限30000次)增加自身最多15点火力值和命中值。"""


class Skill_104711_1(Skill):
    def __init__(self, master):
        """增加自身护甲穿透30%，
        根据总出征数增加自身最多15点命中值"""
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='pierce_coef',
                phase=(AllPhase,),
                value=0.3,
                bias_or_weight=0
            ),
            StatusBuff(
                name='accuracy',
                phase=(AllPhase,),
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_104711_2(CommonSkill):
    """根据总出征数(上限30000次)增加自身最多15点火力值"""
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                name='fire',
                phase=(AllPhase,),
                value=15,
                bias_or_weight=0
            )
        ]


skill = [Skill_104711_1, Skill_104711_2]
