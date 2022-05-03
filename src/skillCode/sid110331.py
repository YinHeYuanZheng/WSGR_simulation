# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 爱宕-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110331(Skill):
    """夜战旗舰(3级)：全队鱼雷值增加5%，索敌增加3点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name="torpedo",
                phase=AllPhase,
                value=0.05,
                bias_or_weight=1
            ),
            StatusBuff(
                timer=timer,
                name="recon",
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            )
        ]


skill = [Skill_110331]
