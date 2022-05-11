# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 威奇塔改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""火力全开(3级)：提升16%的暴击率。当炮击战触发暴击时视为发动技能，技能攻击提升30%的暴击伤害。"""


class Skill_110391(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.16,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=ShellingPhase,
                value=0.3,
                bias_or_weight=0
            )
        ]
