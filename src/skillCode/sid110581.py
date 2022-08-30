# -*- coding: utf-8 -*-
# Author:银河远征
# env:py38
# 高速射击

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""高速射击(3级)：炮击战时40%概率造成1.4倍伤害。"""


class Skill_110581(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.4,
                rate=0.4
            )
        ]


skill = [Skill_110581]
