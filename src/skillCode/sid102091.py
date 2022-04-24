# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 密苏里-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""决胜之兵(3级)：在炮击战阶段优先攻击敌方战列/战巡/航战单位，
增加自身对于战列/战巡/航战的暴击率20%
暴击时攻击无视自身战损。
"""


class Skill_102091(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=ShellingPhase,
                target=OrderedTypeTarget(shiptype=(BB, BC, BBV)),
                ordered=True
            ),
            AtkBuff(
                timer=timer,
                name='crit',
                phase=ShellingPhase,
                value=0.2,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=ShellingPhase,
                atk_request=[BuffRequest_2]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (BB, BC, BBV))


class BuffRequest_2(ATKRequest):
    def __bool__(self):
        return self.atk.get_coef('crit_flag')


skill = [Skill_102091]
