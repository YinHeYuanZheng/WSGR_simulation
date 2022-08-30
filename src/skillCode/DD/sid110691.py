# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 信赖

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自己和位置处于自己上方的一艘舰船的装甲+12，对空+12，回避 +12。(上方指编队界面的左侧)"""


class Skill_110691_1(Skill):
    """自己和位置处于自己上方的一艘舰船的装甲+12，对空+12，回避 +12。(上方指编队界面的左侧)"""
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
                name="armor",
                phase=NightPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name="antiair",
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


name = '不死鸟的守护'
skill = [Skill_110691_1]
