# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 罗德尼-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""攻击时基础火力上升7%，同时降低攻击过的目标15点火力。"""


class Skill_110092(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='give_atk',
                phase=AllPhase,
                buff=[
                    DuringAtkBuff(
                        timer=timer,
                        name='fire',
                        phase=AllPhase,
                        value=0.07,
                        bias_or_weight=1
                    )
                ],
                side=1
            ),
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=AllPhase,
                buff=[
                    StatusBuff(
                        timer=timer,
                        name='fire',
                        phase=AllPhase,
                        value=-15,
                        bias_or_weight=0
                    )
                ],
                side=0
            )
        ]


name = '复仇'
skill = [Skill_110092]
