# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 高雄-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110321(CommonSkill):
    """鱼雷再次装填(3级)：鱼雷值增加36%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name="torpedo",
                phase=AllPhase,
                value=0.36,
                bias_or_weight=1
            )
        ]


skill = [Skill_110321]