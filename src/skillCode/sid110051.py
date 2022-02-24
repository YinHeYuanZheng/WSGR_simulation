# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 日向改-1
from ..wsgr.equipment import DiveBomber
from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110051(Skill):
    """机群驱散T(3级)：降低航空战时对方鱼雷机20%的命中率。"""
    def __init__(self, master):
        super().__init__(master)
        self.target = EquipTarget(side=0,
                                  target=Target(side=0),
                                  equiptype=(DiveBomber,))
        self.buff = [CoeffBuff(
            name='hit_rate',
            phase=(AirPhase,),
            value=-0.2,
            bias_or_weight=0
        )]


skill = [Skill_110051]
