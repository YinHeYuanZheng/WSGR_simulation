# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 列克星敦（cv-2)改-1、萨拉托加改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110291(Skill):
    """航空战术先驱：所有阶段本舰以及相邻位置舰船的舰载机威力上升15%。"""
    def __init__(self, master):
        super().__init__(master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='near',
            master_include=True,
            shiptype=(Aircraft,)
        )

        self.buff = [CoeffBuff(
                name='air_atk_buff',
                phase=(AllPhase,),
                value=0.15,
                bias_or_weight=2
            )]


skill = [Skill_110291]
