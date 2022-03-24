# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 苏联-1

import numpy as np
from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

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
                value=1
            )
        ]


class RandomFinalDamage(FinalDamageBuff):
    def is_active(self, *args, **kwargs):
        self.value = np.random.uniform(0.9, 1.3)
        return isinstance(self.timer.phase, self.phase)


skill = [Skill_102141]
