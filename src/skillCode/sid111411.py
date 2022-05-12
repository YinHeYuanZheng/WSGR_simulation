# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 北安普顿-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_111411(Skill):
    """支援护航(3级)：为自身和相邻船只增加10点回避。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(side=1,
                                       master=master,
                                       radius=1,
                                       direction='near',
                                       master_include=True)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


skill = [Skill_111411]
