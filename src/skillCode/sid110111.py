# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 内华达、俄克拉荷马

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""重点防御(3级)：所有阶段受到攻击时，50%概率发动，减免50%伤害，并且此次攻击不会被暴击。
"""


class Skill_110111(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='get_atk',
                phase=AllPhase,
                buff=[
                    DuringAtkBuff(
                        timer=timer,
                        name='final_damage_debuff',
                        phase=AllPhase,
                        value=-0.5,
                        bias_or_weight=2
                    ),
                    DuringAtkBuff(
                        timer=timer,
                        name='must_not_crit',
                        phase=AllPhase,
                        bias_or_weight=3
                    )
                ],
                side=1,
                rate=0.5
            )
        ]


skill = [Skill_110111]
