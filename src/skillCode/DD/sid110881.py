# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 旁遮普人

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身对潜增加20，战斗中相邻上下单位的回避增加20"""


class Skill_110881_1(CommonSkill):
    """自身对潜增加20"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='antisub',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


class Skill_110881_2(Skill):
    """战斗中相邻上下单位的回避增加20"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='near',
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


name = '船队护航'
skill = [Skill_110881_1, Skill_110881_2]
