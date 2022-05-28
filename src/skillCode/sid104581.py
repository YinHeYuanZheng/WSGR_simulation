# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# U-14

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身 9 点闪避值，闪避值的 20% 同时视为鱼雷值。"""


class Skill_104581_1(Skill):
    """增加自身 9 点闪避值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master, side=1)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=9,
                bias_or_weight=0,
            ),
        ]

class Skill_104581_2(Skill):
    """闪避值的 20% 同时视为鱼雷值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master, side=1)
        #value 将在 activate 具体计算
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=0,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)[0]
        evasion = target.get_final_status('evasion')
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value = evasion * 0.2
                tmp_target.add_buff(tmp_buff)


skill = [Skill_104581_1, Skill_104581_2]
