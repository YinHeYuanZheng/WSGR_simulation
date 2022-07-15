# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 霍埃尔-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""烟雾掩护(3级)：降低上方相邻一个单位30%被攻击概率，并且减少该单位命中值4点"""


class Skill_112781(Skill):
    """降低上方相邻一个单位30%被攻击概率，并且减少该单位命中值4点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='up'
        )
        self.buff = [
            UnMagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.3
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-4,
                bias_or_weight=0
            )
        ]


name = '烟雾掩护'
skill = [Skill_112781]
