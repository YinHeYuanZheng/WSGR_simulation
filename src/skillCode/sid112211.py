# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 飞龙改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_112211(Skill):
    """提升自身18%暴击率"""
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)

        self.buff = [CoeffBuff(
            name='crit',
            phase=(AllPhase,),
            value=0.18,
            bias_or_weight=0
        )]


# todo 降低被命中目标20点火力值
skill = [Skill_112211]
