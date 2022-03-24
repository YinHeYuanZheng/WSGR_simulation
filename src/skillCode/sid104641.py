# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 南达科他(1920)-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""主炮火力(3级)：T优和同航战时，炮击战阶段对大型船造成30%额外伤害。
T劣时增加自身60%暴击率和45%暴击伤害。
"""


class Skill_104641_1(Skill):
    """T优和同航战时，炮击战阶段对大型船造成30%额外伤害。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.3,
                atk_request=[Request_1]
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_direction() == 1 or \
               self.master.get_direction() == 2


class Request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, LargeShip)


class Skill_104641_2(Skill):
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
        return self.master.get_direction() == 4


skill = [Skill_104641_1, Skill_104641_2]
