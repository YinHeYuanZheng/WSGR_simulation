# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 女灶神

"""希望的曙光(3级)：增加自身回避30点，降低自身被攻击概率30%，
    战斗结束后，回复上一场战斗损失耐久最多的船只40%的在上一场的受损耐久。
"""

from src.wsgr.phase import *
from src.wsgr.skill import *


class Skill_103071(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusTarget(
                timer=timer,
                name='evasion',
                phase=(AllPhase,),
                value=30,
            ), UnMagnetBuff(
                timer=timer,
                phase=(AllPhase,),
                rate=0.3,
            )
        ]


skill = [Skill_103071]
