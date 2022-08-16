# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 长春

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""四大金刚(3级)：自身战斗造成伤害提升20%，命中+10"""


class Skill_110971_1(Skill):
    """自身战斗造成伤害提升20%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.2
            )
        ]


class Skill_110971_2(CommonSkill):
    """命中+10"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


name = '四大金刚'
skill = [Skill_110971_1, Skill_110971_2]
