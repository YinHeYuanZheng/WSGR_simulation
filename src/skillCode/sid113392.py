# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 帝国改-2
"""混合特击(3级)：队伍中如果有装母时增加帝国自身18点火力值；炮击战时有25%概率同时对2个单位造成伤害。
"""
from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_113392_1(Skill):
    """队伍中如果有装母时增加帝国自身18点火力值"""
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                name='fire',
                phase=(AirPhase,),
                value=18,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        target_av = TypeTarget(
            side=1,
            shiptype=(AV,)
        ).get_target(friend, enemy)
        return len(target_av) >= 1


# todo 炮击战时有25%概率同时对2个单位造成伤害"""


skill = [Skill_113392_1]
