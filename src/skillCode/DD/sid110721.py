# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 绫波

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""攻击威力不会因耐久损伤而降低，夜战时火力，鱼雷，命中，回避增加 30%。"""


class Skill_110721_1(Skill):
    """攻击威力不会因耐久损伤而降低，夜战时火力，鱼雷，命中，回避增加 30%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=NightPhase,
                value=.3,
                bias_or_weight=1
            ),
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=NightPhase,
                value=.3,
                bias_or_weight=1
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=NightPhase,
                value=.3,
                bias_or_weight=1
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=NightPhase,
                value=.3,
                bias_or_weight=1
            )
        ]


name = '所罗门的鬼神'
skill = [Skill_110721_1]
