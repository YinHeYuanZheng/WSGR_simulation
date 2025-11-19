# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 博格改-1、追赶者改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""降低敌方所有潜艇单位的命中值8点，回避值5点。"""


class Skill_110231_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(SS, SC))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-8,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            )
        ]


name = '反潜护航'
skill = [Skill_110231_1]
