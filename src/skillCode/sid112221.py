# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 苍龙改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110231(Skill):
    """增加自身暴击率10%，被暴击率5%，自身攻击附带25%护甲穿透效果（不能和装备叠加）。"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='crit',
                phase=(AllPhase,),
                value=0.10,
                bias_or_weight=2
            ), CoeffBuff(
                name='',  # todo 被暴击率
                phase=(AllPhase,),
                value=0.05,
                bias_or_weight=2
            ), CoeffBuff(
                name='pierce_coef',
                phase=(AllPhase,),
                value=0.25,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        return True


skill = [Skill_110231]
