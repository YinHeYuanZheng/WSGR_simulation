# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 怨仇-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *

class Skill_104041_1(Skill):
    """钨作战(3级)：降低敌方全体主力舰15闪避值。航空战阶段降低被命中目标15%命中率。"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = TypeTarget(side=0, shiptype=(MainShip, ))
        self.buff = [StatusBuff(
            name='evasion',
            phase=(AllPhase, ),
            value=-15,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        return True


class Skill_104041_2(Skill):
    """航空战阶段降低被命中目标15%命中率。"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = Target()  # todo 被命中目标
        self.buff = [CoeffBuff(
            name='hit_rate',
            phase=(AllPhase, ),
            value=-0.15,
            bias_or_weight=0
        )]


class Request_1(Request):
    def __bool__(self):
        pass


skill = [Skill_104041_1]
