# -*- coding: utf-8 -*-
# Author:银河远征
# env:py38
# 重庆-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import AirAtk

"""防空伪装(3级)：降低80%自身受到的航空攻击的伤害。"""


class Skill_110541(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-0.8,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, AirAtk)


skill = [Skill_110541]
