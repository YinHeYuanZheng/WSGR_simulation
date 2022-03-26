# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 西弗吉尼亚-1
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""苏里高复仇者(3级)：旗舰技，为全队航速27节以下的战列/航战/战巡/重炮提供炮击战加成：攻击时敌人装甲降低20%，T劣时火力值为150%。同时降低自身被攻击概率30%。
"""


class Skill_111101_1(Skill):
    """为全队航速27节以下的战列/航战/战巡/重炮提供炮击战加成：攻击时敌人装甲降低20%，T劣时火力值为150%"""

    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = TypeTarget_1
        self.buff = [
            AtkBuff(
                timer,
                name='ignore_armor',
                value=-0.2,
                phase=ShellingPhase,
                bias_or_weight=1
            ), CoeffBuff(
                timer,
                name='fire_buff',
                phase=ShellingPhase,
                value=0.50,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


class TypeTarget_1(TypeTarget):
    def __init__(self):
        super().__init__(
            side=1,
            shiptype=(BB, BBV, BC, BM)
        )

    def get_target(self, friend, enemy):
        target1 = super().get_target(friend, enemy)
        target = [ship for ship in target1 if ship.speed < 27]
        return target


class Skill_111101_2(Skill):
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


Skill = [Skill_111101_1, Skill_111101_2]
