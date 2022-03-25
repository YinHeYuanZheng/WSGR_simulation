# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 黎塞留-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身暴击率9%。中破、大破或暴击时，攻击无视目标装甲值。"""


class Skill_111132(Skill):

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.09,
                bias_or_weight=0
            ), AtkBuff_1(
                timer=timer
            )
        ]


class AtkBuff_1(AtkBuff):
    def __init__(self, timer):
        super().__init__(timer=timer,
                         name='ignore_armor',
                         phase=AllPhase,
                         value=-1,
                         bias_or_weight=1)

    def is_active(self, *args, **kwargs):
        try:
            atk = kwargs['atk']
        except:
            atk = args[0]

        return self.master.damaged >= 2 or \
            atk.get_coef('crit_flag')


Skill = [Skill_111132]
