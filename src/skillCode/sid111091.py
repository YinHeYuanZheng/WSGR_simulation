# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 马里兰-1
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""好斗的玛丽(3级)：攻击威力不会因耐久损伤而降低，并根据战斗受损程度增加攻击威力，最多28%。。
"""


class Skill_111091(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase,
            ), CoeffBuff(
                timer=timer,
                name='fire_buff',
                phase=AllPhase,
                value=0.28 * (master.status["total_health"] - master.status["health"]) / (
                        master.status["total_health"] - 1),
                bias_or_weight=0
            )
        ]


Skill = [Skill_111091]
