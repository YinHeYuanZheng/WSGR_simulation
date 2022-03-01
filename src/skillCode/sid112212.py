# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 飞龙改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_112212(CommonSkill):
    """突击猛进(3级)：提升自身4点航速和12点火力值，降低自身4点装甲值和5点对空值"""
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
