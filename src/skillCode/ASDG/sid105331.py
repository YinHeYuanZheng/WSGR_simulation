# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 格罗兹尼-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""战斗中免疫受到的第一次攻击。
当队伍里不存在大型船时，自身射程变成长。
队伍中每有一艘S国舰船，战斗中都会为全队舰船增加4点火力值和4%暴击率。"""


class Skill_105331_1(Skill):
    """战斗中免疫受到的第一次攻击"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='shield',
                phase=AllPhase,
                exhaust=1)
        ]


class Skill_105331_2(Skill):
    """当队伍里不存在大型船时，自身射程变成长。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.request = [Request_1]
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            )
        ]


class Request_1(Request):
    def __bool__(self):
        target = TypeTarget(
            side=1,
            shiptype=LargeShip
        ).get_target(self.friend, self.enemy)
        num = len(target)
        return num == 0


class Skill_105331_3(Skill):
    """队伍中每有一艘S国舰船，战斗中都会为全队舰船增加4点火力值和4%暴击率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.04,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        num = len(CountryTarget(side=1, country='S'
                                ).get_target(friend, enemy))
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= num
                tmp_target.add_buff(tmp_buff)


name = '光荣舰队'
skill = [Skill_105331_1, Skill_105331_2, Skill_105331_3]
