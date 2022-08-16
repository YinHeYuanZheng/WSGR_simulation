# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 博格改-1、追赶者改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110231(Skill):
    """降低敌方所有潜艇单位的命中值8点，回避值5点（多个单位携带此技能不重复生效）。"""
    def __init__(self, timer, master):
        # 降低敌方所有潜艇单位的命中值8点，回避值5点（多个单位携带此技能不重复生效）。
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(SS, SC))
        self.buff = [
            UniqueEffect(
                timer=timer,
                effect_type=2.1,
                name='accuracy',
                phase=(AllPhase,),
                value=-8,
                bias_or_weight=0
            ),
            UniqueEffect(
                timer=timer,
                effect_type=2.2,
                name='evasion',
                phase=(AllPhase,),
                value=-5,
                bias_or_weight=0
            )
        ]


name = '反潜护航'
skill = [Skill_110231]
