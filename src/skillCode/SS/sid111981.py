# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# U-505改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""索敌成功时，自身回避值和鱼雷值增加12点。
大破时自身被攻击概率提升100%。
每场战斗免疫1次致命伤害。"""


class Skill_111981_1(Skill):
    """索敌成功时，自身回避值和鱼雷值增加12点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
        ]

    def is_active(self, friend, enemy):
        return self.master.get_recon_flag()


class Skill_111981_2(Skill):
    """大破时自身被攻击概率提升100%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            GreatDamagedMagnet(
                timer=timer,
                phase=AllPhase,
                rate=1,
            )
        ]


class GreatDamagedMagnet(MagnetBuff):
    def is_active(self, atk, *args, **kwargs):
        if super().is_active(atk, *args, **kwargs) and \
                self.master.damaged == 3:
            return True
        else:
            return False


class Skill_111981_3(Skill):
    """每次战斗中能免疫一次致命伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            RecoverShield(timer=timer)
        ]


class RecoverShield(CoeffBuff):
    def __init__(self, timer, phase=AllPhase, name='reduce_damage',
                 value=0, bias_or_weight=0, rate=1):
        super().__init__(timer, name, phase, value, bias_or_weight, rate)
        self.exhaust = 1

    def is_active(self, damage, *args, **kwargs):
        if self.exhaust == 0:
            return False

        master_health = self.master.status['health']
        if damage > master_health:
            self.value = damage - master_health + 1
            self.exhaust -= 1
            return True
        else:
            return False


name = '大难不死的潜艇'
skill = [Skill_111981_1, Skill_111981_2, Skill_111981_3]
