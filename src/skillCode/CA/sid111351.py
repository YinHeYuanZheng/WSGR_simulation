# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 伦敦-1、肯特-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_111351(Skill):
    """过度击穿(3级)：30%概率发动，将单次高于5点的伤害降低为5点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CapShield(
                timer=timer,
                phase=AllPhase,
                cap_value=5,
            ),
        ]


class CapShield(CoeffBuff):
    def __init__(self, timer, phase, cap_value,
                 name='reduce_damage', value=0, bias_or_weight=0, rate=0.3):
        super().__init__(timer, name, phase, value, bias_or_weight, rate)
        self.cap_value = cap_value

    def change_value(self, damage, *args, **kwargs):
        self.value = max(0, damage - self.cap_value)


name = '过度击穿'
skill = [Skill_111351]
