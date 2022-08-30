# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 日向改-1
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.equipment import *


class Skill_110051(Skill):
    """机群驱散T(3级)：降低航空战时对方鱼雷机20%的命中率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=0,
                                  target=Target(side=0),
                                  equiptype=(DiveBomber,))
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=(AirPhase,),
                value=-0.2,
                bias_or_weight=2
            )
        ]


skill = [Skill_110051]
