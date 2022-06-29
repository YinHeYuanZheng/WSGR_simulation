# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 重雷装舰突袭

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""重雷装舰突袭(3级)：解锁开幕雷击，对单个目标造成伤害，威力为鱼雷战的110%。"""


class Skill_103771(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=FirstTorpedoPhase
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=FirstTorpedoPhase,
                value=0.1
            )
        ]


skill = [Skill_103771]
