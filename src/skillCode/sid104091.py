# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 新泽西-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""重火力炮击(3级)：T优时增加自身25%暴击率，同航战时增加自身15%暴击率。
炮击战阶段命中旗舰时造成额外30%伤害。
"""


class Skill_104091_1(Skill):
    """T优时增加自身25%暴击率"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.25,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_direction() == 1


class Skill_104091_2(Skill):
    """同航战时增加自身15%暴击率。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_direction() == 2


class Skill_104091_3(Skill):
    """炮击战阶段命中旗舰时造成额外30%伤害。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.3,
                atk_request=[ATKRequest_1]
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.loc == 1


skill = [Skill_104091_1, Skill_104091_2, Skill_104091_3]
