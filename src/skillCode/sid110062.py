# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 俾斯麦-2
"""永不沉没的战舰(3级)：当前耐久在50%或以上时，受到的所有伤害减少8点。
"""
from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
from src.wsgr.formulas import *


class Skill_110062(Skill):
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [CoeffBuff(
            timer,
            name='reduce_damage',
            phase=AllPhase,
            value=8,
            bias_or_weight=1
        )]

    def is_active(self, friend, enemy):
        return self.master.status['health'] >= self.master.status['total_health'] * 0.25


skill = [Skill_110062]
