# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 突击者改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110281(Skill):
    """弹药整备(3级)：增加25%自身携带的轰炸机威力，降低50%自身携带的鱼雷机威力。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_bomb_atk_buff',
                phase=(AirPhase,),
                value=0.25,
                bias_or_weight=2
            ),
            CoeffBuff(
                timer=timer,
                name='air_dive_atk_buff',
                phase=(AirPhase,),
                value=-0.5,
                bias_or_weight=2
            )
        ]


name = '弹药整备'
skill = [Skill_110281]
