# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 飞龙改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_112211(Skill):
    """提升自身18%暴击率, 降低被命中目标20点火力值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=(AllPhase,),
                value=0.18,
                bias_or_weight=0
            ),
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=(AllPhase,),
                buff=[
                    StatusBuff(
                        timer,
                        name='fire',
                        phase=(AllPhase,),
                        value=-20,
                        bias_or_weight=0
                    )
                ],
                side=0
            )
        ]


name = '舰攻队强袭'
skill = [Skill_112211]
