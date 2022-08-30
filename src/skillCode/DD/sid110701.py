# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 水雷魂

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""鱼雷战和夜战时有 28% 额外概率触发暴击。"""


class Skill_110701_1(Skill):
    """鱼雷战和夜战时有 28% 额外概率触发暴击。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=(NightPhase, SecondTorpedoPhase),
                value=.28,
                bias_or_weight=0
            )
        ]


name = '水雷魂'
skill = [Skill_110701_1]
