# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 新泽西-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
from src.wsgr.formulas import *
"""重火力炮击(3级)：T优时增加自身25%暴击率，同航战时增加自身15%暴击率。炮击战阶段命中旗舰时造成额外30%伤害。
"""


class Skill_104091_1(Skill):
    """T优时增加自身25%暴击率，同航战时增加自身15%暴击率。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        if timer.direction_flag == 1:
            self.buff = [
                CoeffBuff(
                    timer,
                    name='crit',
                    phase=AllPhase,
                    value=0.25,
                    bias_or_weight=0
                )
            ]
        elif timer.direction_flag == 2:
            self.buff = [
                CoeffBuff(
                    timer,
                    name='crit',
                    phase=AllPhase,
                    value=0.15,
                    bias_or_weight=0
                )
            ]


class Skill_104091_2(Skill):
    """炮击战阶段命中旗舰时造成额外30%伤害。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.3,
                atk_request=[ATKRequest_1]
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.loc == 1


skill = [Skill_104091_1, Skill_104091_2]
