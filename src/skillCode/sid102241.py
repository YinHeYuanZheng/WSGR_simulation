# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 可畏-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_102241_1(Skill):
    """马塔潘角之箭(3级)：航空战阶段提升自身15点命中，
    炮击战阶段自身攻击敌人时降低敌人30%的装甲。"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [StatusBuff(
            name='accuracy',
            phase=(AirPhase,),
            value=15,
            bias_or_weight=0
        )
        ]


class Skill_102241_2(Skill):
    """炮击战阶段自身攻击敌人时降低敌人30%的装甲。"""
    # todo 攻击目标检索
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [CoeffBuff(
            name='armor',
            phase=(ShellingPhase,),
            value=-0.3,
            bias_or_weight=2
        )
        ]


class Request_1(Request):
    def __bool__(self):
        pass


skill = [Skill_102241_1, Skill_102241_2]
