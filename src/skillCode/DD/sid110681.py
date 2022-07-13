# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 晓

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""夜战时己方所有舰船命中 +10，增加自身被攻击概率 40%。"""


class Skill_110681_1(Skill):
    """夜战时己方所有舰船命中 +10"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=NightPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_110681_2(Skill):
    """夜战时增加自身被攻击概率 40%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=NightPhase,
                rate=.4,
            )
        ]


name = '强行侦察'
skill = [Skill_110681_1, Skill_110681_2]