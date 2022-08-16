# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 帝国改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_113391(Skill):
    """增加开幕和炮击战阶段伤害20%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer,
                name='final_damage_buff',
                phase=(AirPhase, ShellingPhase),
                value=0.2
            )
        ]


name = '航空曙光'
skill = [Skill_113391]
