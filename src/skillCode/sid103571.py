# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 羽黑-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""第五战队(3级)：队伍中每有一个中型船都会增加自身5点闪避值。
我方所有J系船均增加7点火力值与9%暴击率"""


class Skill_103571_1(Skill):
    """队伍中每有一个中型船都会增加自身5点闪避值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        mid_ship = TypeTarget(side=1, shiptype=MidShip
                              ).get_target(friend, enemy)  # 获取中型船
        buff0 = copy.copy(self.buff[0])
        buff0.value *= len(mid_ship)
        self.master.add_buff(buff0)


class Skill_103571_2(Skill):
    """我方所有J系船均增加7点火力值与9%暴击率"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='J')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=7,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.09,
                bias_or_weight=0
            )
        ]


skill = [Skill_103571_1, Skill_103571_2]
