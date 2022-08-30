# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 声望-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""29节的纳尔逊:首轮炮击命中率增加 10%，最终伤害增加 20%，自身优先攻击排在前方的敌方大型船"""


class Skill_110182(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=FirstShellingPhase,
                value=0.1,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=FirstShellingPhase,
                value=0.2,
            ),
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=FirstShellingPhase,
                target=TypeTarget(side=0, shiptype=LargeShip),
                ordered=True
            )
        ]


name = '29节的纳尔逊'
skill = [Skill_110182]
