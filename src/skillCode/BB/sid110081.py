# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# BIG SEVEN

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""BIG SEVEN(3级)：炮击战时20%概率发动，对2个目标造成116%的伤害。"""


class Skill_110081(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MultipleAtkBuff(
                timer=timer,
                name='multi_attack',
                phase=ShellingPhase,
                num=2,
                rate=0.2,
                coef={'final_damage_buff': 0.16}
            )
        ]


name = 'BIG SEVEN'
skill = [Skill_110081]
