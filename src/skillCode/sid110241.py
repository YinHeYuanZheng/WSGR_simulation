# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 祥凤改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110241_1(Skill):
    """降低敌方队伍内全部轻巡、重巡20点防空值、12点闪避值和12点命中值。"""
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = TypeTarget(side=0, shiptype=('CL', 'CA'))
        self.buff = [StatusBuff(
            name='antiair',
            phase=(AllPhase,),
            value=-20,
            bias_or_weight=0,
        ), StatusBuff(
            name='evasion',
            phase=(AllPhase,),
            value=-12,
            bias_or_weight=0,
        ), StatusBuff(
            name='accuracy',
            phase=(AllPhase,),
            value=-12,
            bias_or_weight=0,
        ), ]


class Skill_110241_2(Skill):
    """炮击战阶段自身受到航母、装母攻击的概率增加20%。"""
    # todo 嘲讽
    def __init__(self, master):
        super().__init__(master)
        self.target = TypeTarget(side=0, shiptype=('CL', 'CA'))
        self.buff = []


skill = [Skill_110241_1, Skill_110241_2]
