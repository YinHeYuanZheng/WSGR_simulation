# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 怨仇-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *

"""钨作战(3级)：降低敌方全体主力舰15闪避值。航空战阶段降低被命中目标15%命中率。"""


class Skill_104041_1(Skill):
    """降低敌方全体主力舰15闪避值"""

    def __init__(self, master):
        super().__init__(master)
        self.target = TypeTarget(side=0, shiptype=(MainShip,))
        self.buff = [StatusBuff(
            name='evasion',
            phase=(AllPhase,),
            value=-15,
            bias_or_weight=0
        )]


class Skill_104041_2(Skill):
    """航空战阶段降低被命中目标15%命中率。"""

    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                name='atk_hit',
                phase=(AirPhase,),
                buff=[
                    CoeffBuff(
                        name='hit_rate',
                        phase=(AirPhase,),
                        value=-0.15,
                        bias_or_weight=0
                    )
                ],
                side=0
            )
        ]


skill = [Skill_104041_1, Skill_104041_2]
