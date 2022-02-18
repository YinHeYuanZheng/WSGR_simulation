# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 企业改-2

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_111212(CommonSkill):
    def __init__(self, master):
        super().__init__(master)

        self.target = SelfTarget(master)

        self.buff = [CommonBuff(
            name='evasion',
            phase=(AllPhase,),
            value=10,
            bias_or_weight=0
        ), CommonBuff(
            name='fire',
            phase=(AllPhase,),
            value=15,
            bias_or_weight=0
        ), CoeffBuff(
            name='crit',
            phase=(AllPhase,),
            value=20,
            bias_or_weight=0
        )]


# todo 炮击战锁头
skill = [Skill_111212]
