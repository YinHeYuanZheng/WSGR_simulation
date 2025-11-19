# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 47工程改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队驱逐舰增加4节航速和12点火力值。"""


class Skill_114161_1(PrepSkill):
    """全队驱逐舰增加4节航速"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=DD)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='speed',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            )
        ]


class Skill_114161_2(Skill):
    """全队驱逐舰增加12点火力值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=DD)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


name = '新起点'
skill = [Skill_114161_1, Skill_114161_2]
