# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 提尔比茨-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""北方的孤独女王(3级)：当提尔比茨作为旗舰时，降低敌方命中和回避8点，
当在出征地图第六章“北海风暴”时，不在旗舰位置也能发动此效果。
"""


class Skill_110071(Skill):
    """当提尔比茨作为旗舰时，降低敌方命中和回避8点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=0)

        self.buff = [
            StatusBuff(
                timer=timer,
                name='hit_rate',
                phase=(AllPhase,),
                value=-8,
                bias_or_weight=0
            ), StatusBuff(
                timer=timer,
                name='miss_rate',
                phase=(AllPhase,),
                value=-8,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


skill = [Skill_110071]
