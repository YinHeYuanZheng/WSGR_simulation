# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# U-96

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""队伍中每有一个潜艇和炮潜单位，都会增加自身3点鱼雷值和4点回避值，昼战阶段自身暴击伤害增加30%。"""


class Skill_112901_1(Skill):
    """队伍中每有一个潜艇和炮潜单位，都会增加自身3点鱼雷值和4点回避值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=3,
                bias_or_weight=0,
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=4,
                bias_or_weight=0,
            ),
        ]

    def activate(self, friend, enemy):
        ss = TypeTarget(side=1, shiptype=(SS, SC)).get_target(friend, enemy)
        count = len(ss)
        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            tmp_buff.value *= count
            self.master.add_buff(tmp_buff)


class Skill_112901_2(Skill):
    """昼战阶段自身暴击伤害增加30%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='crit_coef',
                phase=DaytimePhase,
                value=.3,
                bias_or_weight=0
            ),
        ]


skill = [Skill_112901_1, Skill_112901_2]
