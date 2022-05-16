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
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.6
            )
        ]


env = [EnvSkill_1]
