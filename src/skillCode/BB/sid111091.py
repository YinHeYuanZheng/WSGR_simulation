# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 马里兰-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""好斗的玛丽(3级)：攻击威力不会因耐久损伤而降低，并根据战斗受损程度增加攻击威力，最多28%。"""


class Skill_111091(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase,
            ),
            HealthBasedBuff(
                timer=timer,
                name='power_buff',
                phase=AllPhase,
                value=0.28,
                bias_or_weight=2
            )
        ]


class HealthBasedBuff(CoeffBuff):
    def change_value(self, *args, **kwargs):
        total_health = self.master.status['standard_health']
        health = self.master.status['health']
        self.value = 0.28 * \
                     (total_health - health) / \
                     (total_health - 1)


name = '好斗的玛丽'
skill = [Skill_111091]
