# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 南达科他(1920)-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
from src.wsgr.formulas import *
"""主炮火力(3级)：T优和同航战时，炮击战阶段对大型船造成30%额外伤害。
T劣时增加自身60%暴击率和45%暴击伤害。
"""


class Skill_104601_1(Skill):
    """T优和同航战时，炮击战阶段对大型船造成30%额外伤害。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.3,
                atk_request=[Request_1]
            )
        ]

    def is_active(self, friend, enemy):
        return self.timer.direction_flag <= 2


class Skill_104601_2(Skill):
    """T劣时增加自身60%暴击率和45%暴击伤害。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer,
                name='crit',
                phase=AllPhase,
                value=0.6,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.45,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.timer.direction_flag == 4


class Request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, LargeShip)


skill = [Skill_104601_1, Skill_104601_2]
