# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 加贺改-2

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110231(Skill):
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [StatusBuff(
            name='armor',
            phase=('AllPhase',),
            value=12,
            bias_or_weight=0,
        ), StatusBuff(
            name='antiair',
            phase=('AllPhase',),
            value=12,
            bias_or_weight=0,
        ), ]

    def is_active(self, friend, enemy):
    # todo 判断航速
        return True


class Skill_110231_1(Skill):
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        # todo 应仅为轰炸机系数
        self.buff = [CoeffBuff(
            name='skill_coef',
            phase=('AllPhase',),
            value=20,
            bias_or_weight=2,
        )]

    def is_active(self, friend, enemy):
        # todo 判断航速
        return True


skill = [Skill_110231,Skill_110231_1]
