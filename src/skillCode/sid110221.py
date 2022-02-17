# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 赤城改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill110221(Skill):
    def __init__(self, master):
        super().__init__(master)

        self.target = Target(side=0)

        self.buff = StatusBuff(
            name='antiair',
            phase=(AllPhase,),
            value=-0.3,
            bias_or_weight=1
        )

    def is_active(self, friend, enemy):
        return self.master.loc == 1 and self.timer.recon_flag


skill = [Skill110221]
