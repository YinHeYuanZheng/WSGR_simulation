# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# G6-1
import random

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
"""航空战阶段增加自身40点制空值。
全阶段队伍中随机3艘J国舰船增加10点火力值，对敌方造成的伤害提高15%"""


class Skill_104941_1(Skill):
    """航空战阶段增加自身40点制空值。"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='air_con_buff',
                phase=(AirPhase,),
                value=40,
                bias_or_weight=0
            )
        ]


class Skill_104941_2(Skill):
    """全阶段队伍中随机3艘J国舰船增加10点火力值，对敌方造成的伤害提高15%"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = RandomStatusTarget(
            side=1,
            status_name='country',
            value='J',
        )
        self.buff = [
            StatusBuff(
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                name='final_damage_buff',
                phase=AllPhase,
                value=0.15
            )
        ]


# 仅限g6
class RandomStatusTarget(StatusTarget):
    def __init__(self, side, status_name, value):
        super().__init__(side)
        self.status_name = status_name
        self.value = value

    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = [ship for ship in fleet
                  if ship.get_status(self.status_name) == self.value]

        while len(target) > 3:
            del target[random.randint(0, len(target))]
        return target


class Request_1(Request):
    def __bool__(self):
        pass


skill = [Skill_104941_1]
