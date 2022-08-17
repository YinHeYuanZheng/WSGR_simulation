# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 威尔士亲王-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战攻击时基础火力上升4%，并降低被攻击目标10点回避和10点装甲。"""


class Skill_110102(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=ShellingPhase,
                value=0.04,
                bias_or_weight=1
            ),
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=ShellingPhase,
                buff=[
                    StatusBuff(
                        timer=timer,
                        name='evasion',
                        phase=AllPhase,
                        value=-10,
                        bias_or_weight=0
                    ),
                    StatusBuff(
                        timer=timer,
                        name='armor',
                        phase=AllPhase,
                        value=-10,
                        bias_or_weight=0
                    )
                ],
                side=0
            )
        ]


name = '关键一击'
skill = [Skill_110102]
