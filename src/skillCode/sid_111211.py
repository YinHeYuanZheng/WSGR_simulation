# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 企业改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_111211(Skill):
    def __init__(self, master):
        super().__init__(master)

        self.target = SelfTarget(master)

        self.buff = [CommonBuff(
            name='evasion',
            phase=(AllPhase,),
            value=20,
            bias_or_weight=0
        )]


class Skill_111211_1(Skill):
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.range = 3 - master.status.range
        self.buff = [StatusBuff(
            name='range',
            phase=(AllPhase,),
            value=self.range,
            bias_or_weight=0
        ), StatusBuff(
            name='fire',
            phase=(AllPhase,),
            value=55,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        _target = TypeTarget(side=1, shiptype=('CV', 'CVL', 'AV')).get_target(friend,enemy)
        return len(_target) == 1


skill = [Skill_111211, Skill_111211_1]
