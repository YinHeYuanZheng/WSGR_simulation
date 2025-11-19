# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 伊兹梅尔-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""梯形阵时自身暴击伤害提升20%，攻击敌方战列、战巡时暴击率额外提升25%。"""


class Skill_105401_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            ),
            AtkBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.25,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 4


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (BB, BC))


name = '先锋突进'
skill = [Skill_105401_1]
