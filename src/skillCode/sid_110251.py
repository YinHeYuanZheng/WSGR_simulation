# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 瑞凤改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110251(Skill):
    def __init__(self, master):
        super().__init__(master)
        self.target = TypeTarget(side=0, shiptype=('BB', 'BC'))
        self.buff = [StatusBuff(
            name='antiair',
            phase=('AllPhase',),
            value=15,
            bias_or_weight=0,
        ), StatusBuff(
            name='accuracy',
            phase=('AllPhase',),
            value=9,
            bias_or_weight=0,
        ), ]

    def is_active(self, friend, enemy):
        return len(self.target.get_target()) > 0





skill = [Skill_110251]