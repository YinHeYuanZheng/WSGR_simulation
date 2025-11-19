# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 苏联-1

import numpy as np
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""该船的炮击伤害会在90%~130%之间浮动。"""


class Skill_102141(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            RandomFinalDamage(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0
            )
        ]


class RandomFinalDamage(FinalDamageBuff):
    def change_value(self, *args, **kwargs):
        self.value = np.random.uniform(0.9, 1.3) - 1


skill = [Skill_102141]
