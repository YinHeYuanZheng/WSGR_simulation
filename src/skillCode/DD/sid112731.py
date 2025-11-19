# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 赛尔弗里吉改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队驱逐数量大于敌方时，全队小型船鱼雷值增加20点。
全队驱逐数量不大于敌方时，全队舰船回避值增加20点。
当队伍中护卫舰≥2时，舰队中随机1艘大型船昼战阶段火力值、装甲值、回避值增加15点，并免疫1次伤害。"""


class Skill_112731_1(Skill):
    """全队驱逐数量大于敌方时，全队小型船鱼雷值增加20点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=SmallShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        friend_DD_num = len(TypeTarget(side=1, shiptype=DD).get_target(friend, enemy))
        enemy_DD_num = len(TypeTarget(side=0, shiptype=DD).get_target(friend, enemy))
        return friend_DD_num > enemy_DD_num


class Skill_112731_2(Skill):
    """全队驱逐数量不大于敌方时，全队舰船回避值增加20点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        friend_DD_num = len(TypeTarget(side=1, shiptype=DD).get_target(friend, enemy))
        enemy_DD_num = len(TypeTarget(side=0, shiptype=DD).get_target(friend, enemy))
        return friend_DD_num <= enemy_DD_num


class Skill_112731_3(Skill):
    """当队伍中护卫舰≥2时，舰队中随机1艘大型船昼战阶段火力值、装甲值、回避值增加15点，并免疫1次伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = RandomTypeTarget(side=1, shiptype=LargeShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=DaytimePhase,
                value=15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=DaytimePhase,
                value=15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=DaytimePhase,
                value=15,
                bias_or_weight=0
            ),
            DamageShield(
                timer=timer,
                phase=DaytimePhase
            )
        ]

    def is_active(self, friend, enemy):
        cover_num = len(TypeTarget(side=1, shiptype=CoverShip
                                   ).get_target(friend, enemy))
        return cover_num >= 2


name = '驱逐领队'
skill = [Skill_112731_1, Skill_112731_2, Skill_112731_3]
