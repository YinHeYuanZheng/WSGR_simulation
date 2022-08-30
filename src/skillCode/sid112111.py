# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 卡约•杜伊里奥-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""幸运之舰(3级)：首轮炮击额外提升最低20%，最高25%的伤害。
被攻击时增加幸运值20%的装甲值。
"""


class Skill_112111(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            RandomFinalDamage(
                timer=timer,
                name='final_damage_buff',
                phase=FirstShellingPhase,
                value=0
            ),
            LuckBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=0,
                bias_or_weight=0
            )
        ]


class RandomFinalDamage(FinalDamageBuff):
    def is_active(self, *args, **kwargs):
        self.value = np.random.uniform(0.2, 0.25)
        return isinstance(self.timer.phase, self.phase)


class LuckBuff(StatusBuff):
    def is_active(self, *args, **kwargs):
        self.value = np.ceil(0.2 * self.master.get_final_status('luck'))
        return isinstance(self.timer.phase, self.phase)


skill = [Skill_112111]
