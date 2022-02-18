# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 瑞凤改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
"""直卫空母(3级)：降低敌方全体战列、战巡的对空值15点、命中值9点。
"""


class Skill_110251(Skill):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = TypeTarget(side=0, shiptype=('BB', 'BC'))
        self.buff = [StatusBuff(
            name='antiair',
            phase=('AllPhase',),
            value=-15,
            bias_or_weight=0,
        ), StatusBuff(
            name='accuracy',
            phase=('AllPhase',),
            value=-9,
            bias_or_weight=0,
        ), ]

    def is_active(self, friend, enemy):
        return len(self.target.get_target()) > 0





skill = [Skill_110251]