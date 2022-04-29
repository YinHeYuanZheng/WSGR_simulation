# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 胡德-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身作为旗舰时，提升全队航速 4 点。"""


class Skill_110012(PrepSkill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='speed',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


skill = [Skill_110012]
