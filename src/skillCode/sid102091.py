# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 密苏里-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
"""决胜之兵(3级)：在炮击战阶段优先攻击敌方战列/战巡/航战单位，
增加自身对于战列/战巡/航战的暴击率20%
暴击时攻击无视自身战损。
"""


class Skill_102091_1(Skill):
    """在炮击战阶段优先攻击敌方战列/战巡/航战单位，"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=(ShellingPhase,),
                target=OrderedTypeTarget(shiptype=(BB, BC, BBV)),
                ordered=True
            ),
        ]

    def is_active(self, friend, enemy):
        return True


class Skill_102091_2(Skill):
    """增加自身对于战列/战巡/航战的暴击率20%"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer,
                name="crit",
                phase=ShellingPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.request[0](self.timer, self.master.atk)


class Skill_102091_3(Skill):
    """暴击时攻击无视自身战损。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.atk_request = [atk_request_1]
        self.buff = [
            SpecialBuff(
                timer,
                name="ignore_damaged",
                phase=ShellingPhase,
                atk_request=self.atk_request
            )
        ]

    def is_active(self, friend, enemy):
        return True


class atk_request_1(ATKRequest):
    def __bool__(self):
        return self.atk.get_coef('crit_flag')


class Request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (BB, BC, BBV))


skill = [Skill_102091_1, Skill_102091_3]
