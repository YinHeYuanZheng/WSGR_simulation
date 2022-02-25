# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# G15-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
"""增加自身火力值5/10/15点、航速1/2/3节。
航空战阶段自身被攻击概率提高20%/30%/40%，受到伤害减少7/11/15点。"""


class Skill_104861_1(CommonSkill):
    """增加自身火力值5/10/15点、航速1/2/3节。"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0,
            ),
            CommonBuff(
                name='speed',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            )
        ]


class Skill_104861_2(Skill):
    # todo 航空战嘲讽
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = []


class Skill_104861_3(Skill):
    # todo 固定减伤
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = []


class Request_1(Request):
    def __bool__(self):
        pass


skill = [Skill_104861_1]
