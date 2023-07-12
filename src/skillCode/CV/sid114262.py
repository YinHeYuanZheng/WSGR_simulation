# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 彼得·施特拉塞尔改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队舰船索敌值增加3点。炮击战阶段全队舰船造成的伤害提升20%。
当敌方主力舰≥3时，自身优先攻击敌方耐久值最高的单位，攻击时无视目标100%对空值（不包含装备）。"""


class Skill_114262_1(PrepSkill):
    """全队索敌值增加3点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=3,
                bias_or_weight=0,
            ),
        ]


class Skill_114262_2(Skill):
    """炮击战阶段全队舰船造成的伤害提升20%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.2
            )
        ]


class Skill_114262_3(Skill):
    """当敌方主力舰≥3时，自身优先攻击敌方耐久值最高的单位，攻击时无视目标100%对空值（不包含装备）"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_loc_target',
                phase=ShellingPhase,
                target=HighestTarget(side=0),
                ordered=True
            ),
            AtkBuff(
                timer=timer,
                name='ignore_antiair',
                phase=AllPhase,
                value=-1,
                bias_or_weight=1,
            )
        ]

    def is_active(self, friend, enemy):
        target = TypeTarget(
            side=0,
            shiptype=MainShip
        ).get_target(friend, enemy)
        number = len(target)
        return number >= 3



class HighestTarget(Target):
    def get_target(self, friend, enemy):
        fleet = self.get_target_fleet(friend, enemy)
        fleet.sort(key=lambda x: -x.status['health'])
        return fleet


name = '帝国荣光'
skill = [Skill_114262_1, Skill_114262_2, Skill_114262_3]
