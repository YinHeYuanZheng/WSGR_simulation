# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 胜利改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身及相邻舰船的20%暴击率，自身及相邻装母舰载机威力提升15%"""


class Skill_114832_1(Skill):
    """增加自身及相邻舰船的20%暴击率"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='near',
            master_include=True
        )

        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]


class Skill_114832_2(Skill):
    """自身及相邻装母舰载机威力提升15%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='near',
            master_include=True,
            shiptype=AV
        )

        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=2
            )
        ]


name = '喷气突击队'
skill = [Skill_114832_1, Skill_114832_2]

