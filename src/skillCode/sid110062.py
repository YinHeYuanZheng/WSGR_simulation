# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 俾斯麦-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""永不沉没的战舰(3级)：当前耐久在50%或以上时，受到的所有伤害减少8点。
"""


class Skill_110062(Skill):
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='reduce_damage',
                phase=AllPhase,
                value=8,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.damaged == 1


skill = [Skill_110062]
