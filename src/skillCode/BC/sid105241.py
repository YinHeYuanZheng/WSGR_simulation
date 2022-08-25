# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 夏威夷-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身攻击敌方战巡、重巡、轻巡时，伤害和暴击率提升30%。
降低敌方护卫舰12点命中值、回避值和装甲值。"""


class Skill_105241_1(Skill):
    """自身攻击敌方战巡、重巡、轻巡时，伤害和暴击率提升30%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.3,
                atk_request=[ATKRequest_1]
            ),
            AtkBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0,
                atk_request=[ATKRequest_1]
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (BC, CA, CL))


class Skill_105241_2(Skill):
    """降低敌方护卫舰12点命中值、回避值和装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=CoverShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-12,
                bias_or_weight=0
            ),
        ]


name = '巡洋压制'
skill = [Skill_105241_1, Skill_105241_2]
