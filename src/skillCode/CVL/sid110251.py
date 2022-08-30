# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 瑞凤改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110251(Skill):
    """直卫空母(3级)：降低敌方全体战列、战巡的对空值15点、命中值9点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(BB, BC))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=(AllPhase,),
                value=-15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=(AllPhase,),
                value=-9,
                bias_or_weight=0
            ),
        ]


name = '直卫空母'
skill = [Skill_110251]
