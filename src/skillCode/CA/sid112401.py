# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 旧金山改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""久经战阵(3级)：
队伍中战列数量等于或低于敌方时，提升队伍里大型船12点命中值、中型船10点火力值、小型船20%暴击率。
队伍中战列数量高于敌方时，提升队伍里大型船15点对空值、中型船20点装甲值，小型船13点闪避值。
自身级别每提升10级增加3点装甲值
"""


class Skill_112401_1(Skill):
    """队伍中战列数量等于或低于敌方时，提升队伍里大型船12点命中值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.request = [Request_1]
        self.target = TypeTarget(side=1, shiptype=LargeShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


class Skill_112401_2(Skill):
    """队伍中战列数量等于或低于敌方时，提升队伍里中型船10点火力值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.request = [Request_1]
        self.target = TypeTarget(side=1, shiptype=MidShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_112401_3(Skill):
    """队伍中战列数量等于或低于敌方时，提升队伍里小型船20%暴击率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.request = [Request_1]
        self.target = TypeTarget(side=1, shiptype=SmallShip)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]


class Request_1(Request):
    def __bool__(self):
        friend_bb = TypeTarget(side=1, shiptype=BB
                               ).get_target(self.friend, self.enemy)
        enemy_bb = TypeTarget(side=0, shiptype=BB
                              ).get_target(self.friend, self.enemy)
        return len(friend_bb) <= len(enemy_bb)


class Skill_112401_4(Skill):
    """队伍中战列数量高于敌方时，提升队伍里大型船15点对空值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.request = [Request_2]
        self.target = TypeTarget(side=1, shiptype=LargeShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_112401_5(Skill):
    """队伍中战列数量高于敌方时，提升队伍里中型船20点装甲值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.request = [Request_2]
        self.target = TypeTarget(side=1, shiptype=MidShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


class Skill_112401_6(Skill):
    """队伍中战列数量高于敌方时，提升队伍里小型船13点闪避值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.request = [Request_2]
        self.target = TypeTarget(side=1, shiptype=SmallShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=13,
                bias_or_weight=0
            )
        ]


class Request_2(Request):
    def __bool__(self):
        friend_bb = TypeTarget(side=1, shiptype=BB
                               ).get_target(self.friend, self.enemy)
        enemy_bb = TypeTarget(side=0, shiptype=BB
                              ).get_target(self.friend, self.enemy)
        return len(friend_bb) > len(enemy_bb)


class Skill_112401_7(Skill):
    """自身级别每提升10级增加3点装甲值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=3 * int(self.master.level / 10),
                bias_or_weight=0
            )
        ]


name = '久经战阵'
skill = [Skill_112401_1, Skill_112401_2, Skill_112401_3,
         Skill_112401_4, Skill_112401_5, Skill_112401_6, Skill_112401_7]
