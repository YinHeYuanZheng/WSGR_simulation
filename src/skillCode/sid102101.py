# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 衣阿华-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

"""止战之戈(3级)：炮击战阶段，26%概率炮击同一个目标两次，触发技能之后炮击战阶段将不再行动。"""


class Skill_102101(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            ExtraAtkBuff(
                timer=timer,
                name='extra_attack',
                phase=ShellingPhase,
                num=2,
                rate=0.26,
                end_buff=[
                    ActPhaseBuff(
                        timer=timer,
                        name='not_act_phase',
                        phase=ShellingPhase
                    )
                ]
            )
        ]


skill = [Skill_102101]
