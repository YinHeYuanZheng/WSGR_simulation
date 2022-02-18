# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 飞龙改-2

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_112212(CommonSkill):
    def __init__(self, master):
        super().__init__(master)

        self.target = SelfTarget(master)

        self.buff = [CommonBuff(
            name='speed',
            phase=(AllPhase,),
            value=4,
            bias_or_weight=0
        ), CommonBuff(
            name='fire',
            phase=(AllPhase,),
            value=12,
            bias_or_weight=0
        ), CommonBuff(
            name='armor',
            phase=(AllPhase,),
            value=-4,
            bias_or_weight=0
        ), CommonBuff(
            name='antiair',
            phase=(AllPhase,),
            value=-5,
            bias_or_weight=0
        )]


skill = [Skill_112212]
