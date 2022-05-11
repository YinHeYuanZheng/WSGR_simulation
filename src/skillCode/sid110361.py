# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 希佩尔海军上将-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110361(Skill):
    """伪装奇袭(3级)：炮击战时30%概率发动，攻击敌舰队中的驱逐舰且必定命中。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name="give_atk",
                phase=ShellingPhase,
                buff=[
                    SpecialBuff(
                        timer=timer,
                        name="must_hit",
                        phase=ShellingPhase,
                    ),
                    PriorTargetBuff(
                        timer=timer,
                        name="prior_type_target",
                        phase=ShellingPhase,
                        target=DD,
                        ordered=True
                    )
                ],
                side=1,
                rate=0.3
            )
        ]


skill = [Skill_110361]
