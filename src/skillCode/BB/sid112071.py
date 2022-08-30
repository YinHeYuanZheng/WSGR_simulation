# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 南达科他-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""不屈的迎风花(3级)：增加自身30%被攻击概率，
提升两侧友方单位18%暴击率，
自身中破、大破状态下无法参与任何攻击。
"""


class Skill_112071_1(Skill):
    """增加自身30%被攻击概率
    自身中破、大破状态下无法参与任何攻击"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=(AllPhase,),
                rate=0.3
            ),
            ActPhaseBuff_1(
                timer=timer,
                name='not_act_phase',
                phase=AllPhase
            )
        ]


class Skill_112071_2(Skill):
    """提升两侧友方单位18%暴击率"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='near',
        )

        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=(AllPhase,),
                value=0.18,
                bias_or_weight=0
            )
        ]


class ActPhaseBuff_1(ActPhaseBuff):
    def is_active(self, *args, **kwargs):
        return self.master.damaged >= 2


name = '不屈的迎风花'
skill = [Skill_112071_1, Skill_112071_2]
