# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 1938(I)-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战阶段自身护甲穿透增加40%。队伍中每有一艘U国舰船都会增加自身5点火力值。"""


class Skill_105601_1(Skill):
    """炮击战阶段自身护甲穿透增加40%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='pierce_coef',
                phase=ShellingPhase,
                value=0.4,
                bias_or_weight=0
            )
        ]


class Skill_105601_2(Skill):
    """队伍中每有一艘U国舰船都会增加自身5点火力值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=ShellingPhase,
                value=5,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        buff_0 = copy.copy(self.buff[0])
        u_bb = CountryTarget(side=1, country='U').get_target(friend, enemy)
        buff_0.value *= len(u_bb)
        self.master.add_buff(buff_0)


name = 'A级火力'
skill = [Skill_105601_1, Skill_105601_2]
