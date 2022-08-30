# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 皇家方舟-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_101191(Skill):
    """精准打击(3级)：皇家方舟攻击命中的敌人：回避降低30，被暴击率提升25%。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer,
                name='atk_hit',
                phase=(AllPhase,),
                buff=[
                    StatusBuff(
                        timer,
                        name='evasion',
                        phase=(AllPhase,),
                        value=-30,
                        bias_or_weight=0
                    ),
                    CoeffBuff(
                        timer,
                        name='be_crit',
                        phase=(AllPhase,),
                        value=0.25,
                        bias_or_weight=0
                    )
                ],
                side=0
            )
        ]


skill = [Skill_101191]
