# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 巴夫勒尔

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""新锐装备(3级)：自身在航空战阶段受到伤害减少80%；鱼雷战阶段额外发射一枚鱼雷，伤害为正常的85%。
"""


class Skill_113061(Skill):
    """自身在航空战阶段受到伤害减少80%；鱼雷战阶段额外发射一枚鱼雷，伤害为正常的85%。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AirPhase,
                value=-0.8,
            ),
            MultipleAtkBuff(
                timer=timer,
                name='multi_attack',
                phase=TorpedoPhase,
                rate=0.85,
            )
        ]

name = "新锐装备"
skill = [Skill_113061]
