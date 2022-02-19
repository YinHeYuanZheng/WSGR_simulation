# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 大凤改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

"""全阶段降低敌方旗舰40点火力值和40点命中值,
降低敌方主力舰20点火力值和20点装甲值,
降低敌方护卫舰15点闪避值和20点对空值。
"""


#todo 对象检索
class Skill_111171(Skill):
    def __init__(self, master):
        # 全阶段降低敌方旗舰40点火力值和40点命中值,
        super().__init__(master)
        self.master = master
        self.target = Target(master)
        self.buff = [
            StatusBuff(
                name='fire',
                phase=('AllPhase', ),
                value=-40,
                bias_or_weight=0
            ), StatusBuff(
                name='accuracy',
                phase=('AllPhase', ),
                value=-40,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return True


class Skill_111171_1(Skill):
    def __init__(self, master):
        # 降低敌方护卫舰15点闪避值和20点对空值。
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [StatusBuff(
                name='evasion',
                phase=('AllPhase', ),
                value=-15,
                bias_or_weight=0
            ),
            StatusBuff(
                name='antiair',
                phase=('AllPhase', ),
                value=-20,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return True


class Skill_111171_2(Skill):
    def __init__(self, master):
        #降低敌方主力舰20点火力值和20点装甲值,
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [StatusBuff(
            name='fire',
            phase=('AllPhase',),
            value=-20,
            bias_or_weight=0
        ), StatusBuff(
            name='armor',
            phase=('AllPhase',),
            value=-20,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        return True


skill = [Skill_111171, Skill_111171_1, Skill_111171_2]