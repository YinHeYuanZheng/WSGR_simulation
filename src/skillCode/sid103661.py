# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 鹦鹉螺

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""提升自身和自身相邻上方一艘船 9 点闪避值和 9 点装甲值。提升自身火力 *0.5% 的暴击率。"""


class Skill_103661_1(Skill):
    """提升自身和自身相邻上方一艘船 9 点闪避值和 9 点装甲值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='up',
            master_include=True,
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=9,
                bias_or_weight=0,
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]


class Skill_103661_2(Skill):
    """提升自身火力 *0.5% 的暴击率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master, side=1)
        #value will be calculated in function activate
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)[0]
        fire = target.get_final_status('fire')
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value = fire * 0.005
                tmp_target.add_buff(tmp_buff)


skill = [Skill_103661_1, Skill_103661_2]
