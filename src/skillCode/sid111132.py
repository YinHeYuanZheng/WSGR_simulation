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
            ),
            AtkBuff(
                timer=timer,
                name='ignore_armor',
                phase=AllPhase,
                value=-1,
                bias_or_weight=1,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        if self.atk.atk_body.damaged == 2 or \
                self.atk.atk_body.damaged == 3:
            return True
        if self.atk.get_coef('crit_flag'):
            return True

        return False


skill = [Skill_111132]
