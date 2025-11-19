# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 空想

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全阶段受到攻击时有25%概率免疫所有伤害。"""


class Skill_110991(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-1,
                rate=0.25
            )
        ]


name = '高速机动'
skill = [Skill_110991]
