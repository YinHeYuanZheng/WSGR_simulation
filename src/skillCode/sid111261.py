# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 普林斯顿改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
"""帽子戏法(3级)：战斗机对空值+30%，战斗中鱼雷机威力+15%。
"""


class Skill_111261(Skill):
    def __init__(self, master):
        """todo 战斗机对空值+30%，"""
        # 战斗中鱼雷机威力+15%。
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [CoeffBuff(
            name='air_dive_atk_buff',
            phase=('AirPhase', ),
            value=0.15,
            bias_or_weight=2
        )]

    def is_active(self, friend, enemy):
        return True


skill = [Skill_111261]
