# -*- coding:utf-8 -*-
# Author:huan_yp
# Edited by: 银河远征(20260410)
# env:py38
# 无敌-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""冲锋(3级)：非梯形阵时自身装甲值和回避值增加30点，暴击率提高20%。
梯形阵时自身被攻击概率提高20%，攻击必定暴击且无视战损，暴击伤害增加50%。
"""


class Skill_104611_1(Skill):
    """非梯形阵时自身装甲值和回避值增加30点，暴击率提高20%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() != 4


class Skill_104611_2(Skill):
    """梯形阵时自身被攻击概率提高20%，攻击必定暴击且无视战损，暴击伤害增加50%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.2,
            ),
            SpecialBuff(
                timer=timer,
                name='must_crit',
                phase=AllPhase,
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase,
            ),
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.5,
                bias_or_weight=0,
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 4


name = '冲锋'
skill = [Skill_104611_1, Skill_104611_2]
