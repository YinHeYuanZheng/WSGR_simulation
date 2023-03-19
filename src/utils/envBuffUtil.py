# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 环境加成

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class AllTarget(Target):
    """针对双方全体(可指定筛选类型)"""

    def __init__(self, side=None, target: Target = None):
        super().__init__(side)
        self.target = target

    def get_target(self, friend, enemy):
        if self.target is not None:
            target_1 = self.target.get_target(friend, enemy)
            target_0 = self.target.get_target(enemy, friend)
            return target_1 + target_0
        else:
            if isinstance(friend, Fleet):
                friend = friend.ship
            if isinstance(enemy, Fleet):
                enemy = enemy.ship
            return friend + enemy


class EnvSkill_1(Skill):
    """猪飞：大型船伤害+60%"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=LargeShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.6
            )
        ]


class EnvSkill_2(Skill):
    """猪飞：中型船伤害+60%"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=MidShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.6
            )
        ]


class EnvSkill_3(Skill):
    """猪飞：小型船伤害+60%"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=SmallShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.6
            )
        ]


class EnvSkill_4(Skill):
    """航巡全阶段必中"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=CAV)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='must_hit',
                phase=AllPhase
            )
        ]


env = []
