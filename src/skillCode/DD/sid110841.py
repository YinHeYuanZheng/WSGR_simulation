# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 天后

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import TorpedoAtk

"""对潜艇攻击时命中率提高30%，被鱼雷攻击时回避率提高30。"""


class Skill_110841(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0,
                atk_request=[ATK_Request_1]
            ),
            AtkBuff(
                timer=timer,
                name='miss_rate',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0,
                atk_request=[ATK_Request_2]
            )
        ]


class ATK_Request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, SS)


class ATK_Request_2(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, TorpedoAtk)


name = '对潜专精'
skill = [Skill_110841]
