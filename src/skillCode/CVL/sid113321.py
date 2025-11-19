# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 神鹰改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import TorpedoAtk

"""全队对鱼雷攻击的回避率提高30%，受到的鱼雷伤害降低60%。
自身攻击护卫舰时伤害提高30%，攻击潜艇时命中率提高30%。"""


class Skill_113321_1(Skill):
    """全队对鱼雷攻击的回避率提高30%，受到的鱼雷伤害降低60%。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='miss_rate',
                phase=AllPhase,
                value=.3,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-.6,
                atk_request=[BuffRequest_1]
            ),
        ]


class Skill_113321_2(Skill):
    """自身攻击护卫舰时伤害提高30%，攻击潜艇时命中率提高30%。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=.3,
                atk_request=[BuffRequest_2]
            ),
            AtkBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=.3,
                bias_or_weight=0,
                atk_request=[BuffRequest_3]
            ),
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, TorpedoAtk)


class BuffRequest_2(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, CoverShip)


class BuffRequest_3(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, SS)


name = '反潜护卫'
skill = [Skill_113321_1, Skill_113321_2]
