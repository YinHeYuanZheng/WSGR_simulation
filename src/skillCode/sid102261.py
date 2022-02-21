# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 埃塞克斯-1
import random

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_102261_1(CommonSkill):
    """猎火鸡比赛(3级)：提升自身6点火力值。
    战斗中当敌方有装母、航母或者轻母时，随机降低敌方一艘装母、航母或者轻母的火力值20点。"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [CommonBuff(
            name='fire',
            phase=(AllPhase, ),
            value=6,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        return True


class Skill_102261_2(CommonSkill):
    """战斗中当敌方有装母、航母或者轻母时，随机降低敌方一艘装母、航母或者轻母的火力值20点。"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = RandomTarget(side=0,
                                   shiptype=(Aircraft,))
        self.buff = [StatusBuff(
            name='fire',
            phase=(AllPhase, ),
            value=-20,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        return True


class RandomTarget(TypeTarget):
    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = [ship for ship in fleet if isinstance(ship, self.shiptype)]
        target = target[random.randint(0, len(target) - 1)]
        return target


class Request_1(Request):
    def __bool__(self):
        pass


skill = [Skill_102261_1]
