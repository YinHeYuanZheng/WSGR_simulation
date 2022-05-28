# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 长春

"""四大金刚(3级)：自身战斗造成伤害提升15%，命中+10，演习获得经验提升15%。
"""


from src.wsgr.phase import *
from src.wsgr.skill import *


class Skill_110971(Skill):
    """自身战斗造成伤害提升15%，命中+10"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.15
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


skill = [Skill_110971]
