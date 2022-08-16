# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 鹦鹉螺-1

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
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.005,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        fire = self.master.get_final_status('fire')
        buff0 = copy.copy(self.buff[0])
        buff0.value *= fire
        self.master.add_buff(buff0)


name = '秘密潜行'
skill = [Skill_103661_1, Skill_103661_2]
