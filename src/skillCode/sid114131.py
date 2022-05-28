# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 加里波第

"""北极星威慑(3级)：炮击战阶段自身命中过的目标不再行动(限炮击战阶段)。
    炮击战阶段有70%概率增加最小30%，最多100%的额外伤害。本角色无法装备大口径主炮。"""

import numpy
from src.wsgr.phase import *
from src.wsgr.skill import *


class Skill_114131_1(Skill):
    """炮击战阶段自身命中过的目标不再行动(限炮击战阶段)"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=(ShellingPhase,),
                buff=[
                    ActPhaseBuff(
                        timer,
                        name='not_act_phase',
                        phase=(ShellingPhase,)
                    )
                ],
                side=0
            )
        ]

class Skill_114131_2(Skill):
    """炮击战阶段有70%概率增加最小30%，最多100%的额外伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                phase=ShellingPhase,
                value=numpy.random.uniform(0.3, 1),
                rate=0.7
            )
        ]

skill = [Skill_114131_1, Skill_114131_2]


