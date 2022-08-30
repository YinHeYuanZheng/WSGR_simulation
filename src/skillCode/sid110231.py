# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 加贺改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110231(Skill):
    """开幕航空战阶段提升自身12%暴击率，炮击战阶段提升自身命中率12%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=(AirPhase,),
                value=0.12,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=(ShellingPhase,),
                value=0.12,
                bias_or_weight=2
            )
        ]


skill = [Skill_110231]
