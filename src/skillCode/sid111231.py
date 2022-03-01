# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 博格改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110231(Skill):
    """降低敌方所有潜艇单位的命中值8点，回避值5点 todo（多个单位携带此技能不重复生效）。"""
    def __init__(self, timer, master):
        # 降低敌方所有潜艇单位的命中值8点，回避值5点（多个单位携带此技能不重复生效）。
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(SS, SC))
        self.buff = [
            StatusBuff(
                timer,
                name='accuracy',
                phase=(AllPhase,),
                value=-8,
                bias_or_weight=0
            ),
            StatusBuff(
                timer,
                name='evasion',
                phase=(AllPhase,),
                value=-5,
                bias_or_weight=0
            )
        ]


skill = [Skill_110231]
