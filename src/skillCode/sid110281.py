# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 突击者改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110281(Skill):
    """弹药整备(3级)：增加25%自身携带的轰炸机威力，降低50%自身携带的鱼雷机威力。"""
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='air_bomb_atk_buff',
                phase=(AirPhase,),
                value=0.25,
                bias_or_weight=2
            ),
            CoeffBuff(
                name='air_dive_atk_buff',
                phase=(AirPhase,),
                value=-0.5,
                bias_or_weight=2
            )
        ]


skill = [Skill_110281]
