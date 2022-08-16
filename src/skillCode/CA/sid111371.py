# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 波特兰改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""善战者(3级)：根据总出征次数（上限20000次）增加自己火力值最多18点，对空值最多18。"""


class Skill_111371(Skill):
    """增加自己火力值最多18点，对空值最多18"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=18,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=18,
                bias_or_weight=0
            )
        ]


name = '善战者'
skill = [Skill_111371]
