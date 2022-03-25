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
    """首轮炮击额外提升最低20%，最高25%的伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=(ShellingPhase,),
                value=np.random.uniform(.2, .25)
            ), StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=0.2 * self.master.get_final_status('luck'),
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


skill = [Skill_112111]
