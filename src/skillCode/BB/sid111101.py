# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 西弗吉尼亚-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""苏里高复仇者(3级)：旗舰技，为全队航速27节以下的战列/航战/战巡/重炮提供炮击战加成：
攻击时敌人装甲降低20%，T劣时火力值为150%。
同时降低自身被攻击概率30%。
"""


class Skill_111101_1(Skill):
    """旗舰技，为全队航速27节以下的战列/航战/战巡/重炮提供炮击战加成：
    攻击时敌人装甲降低20%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeStatusTarget(
            side=1,
            shiptype=(BB, BBV, BC, BM)
        )

        self.buff = [
            CoeffBuff(
                timer=timer,
                name='ignore_armor',
                value=-0.2,
                phase=ShellingPhase,
                bias_or_weight=1
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


class Skill_111101_2(Skill):
    """旗舰技，为全队航速27节以下的战列/航战/战巡/重炮提供炮击战加成：
    T劣时火力值为150%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeStatusTarget(
            side=1,
            shiptype=(BB, BBV, BC, BM)
        )

        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=ShellingPhase,
                value=0.50,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1 and \
               self.master.get_dir_flag() == 4


class TypeStatusTarget(TypeTarget):
    def get_target(self, friend, enemy):
        fleet = self.get_target_fleet(friend, enemy)
        target = []
        for ship in fleet:
            if isinstance(ship, self.shiptype) and \
                    ship.get_final_status('speed') <= 27:
                target.append(ship)
        return target


class Skill_111101_3(Skill):
    """同时降低自身被攻击概率30%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            UnMagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.3
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


name = '苏里高复仇者'
skill = [Skill_111101_1, Skill_111101_2, Skill_111101_3]
