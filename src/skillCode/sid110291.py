# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 列克星敦（cv-2)改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110231(Skill):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        # todo 目标选择
        self.target = LocTarget(master)

        self.buff = [CoeffBuff(
                name='air_atk_buff',
                phase=(AirPhase,),
                value=0.15,
                bias_or_weight=2
            )]

    def is_active(self, friend, enemy):
        return True


skill = [Skill_110231]