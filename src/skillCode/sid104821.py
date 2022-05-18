# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 大淀(苍青)-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加全队舰船先制鱼雷和鱼雷战20%暴击率，增加全队舰船8点索敌值。"""


class Skill_104821_1(Skill):
    """增加全队舰船先制鱼雷和鱼雷战20%暴击率"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=TorpedoPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]


class Skill_104821_2(PrepSkill):
    """增加全队舰船8点索敌值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            )
        ]


skill = [Skill_104821_1, Skill_104821_2]
