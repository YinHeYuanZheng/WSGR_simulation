# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 贝亚恩改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""队伍中存在战列舰时，提高全队F国舰船8%暴击率。
队伍中存在护卫舰时，增加自身30点制空值。"""


class Skill_112321_1(Skill):
    """队伍中存在战列舰时，提高全队F国舰船8%暴击率。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='F')
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.08,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        num_bb = len(TypeTarget(side=1, shiptype=BB).get_target(friend, enemy))
        return num_bb


class Skill_112321_2(Skill):
    """队伍中存在护卫舰时，增加自身30点制空值。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_con_buff',
                phase=AirPhase,
                value=30,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        num_cover = len(TypeTarget(side=1, shiptype=CoverShip).get_target(friend, enemy))
        return num_cover


name = '海航先锋'
skill = [Skill_112321_1, Skill_112321_2]
