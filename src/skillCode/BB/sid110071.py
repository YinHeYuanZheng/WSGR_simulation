# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 提尔比茨-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""降低敌方12点命中值和回避值。
当俾斯麦处于编队中时，提高自身12点火力值、装甲值、命中值。"""


class Skill_110071_1(Skill):
    """降低敌方12点命中值和回避值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=0)
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
            )
        ]

    # def is_active(self, friend, enemy):
    #     return self.master.loc == 1


class Skill_110071_2(Skill):
    """当俾斯麦处于编队中时，提高自身12点火力值、装甲值、命中值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
        ]

    def is_active(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        for tmp_ship in friend:
            if tmp_ship.cid == '10006' or tmp_ship.cid == '11006':
                return True
        return False


name = '北方的孤独女王'
skill = [Skill_110071_1, Skill_110071_2]
