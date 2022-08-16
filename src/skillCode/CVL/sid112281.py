# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 隼鹰改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_112281(Skill):
    """对敌方航母，装甲航母，轻母造成的最终伤害增加25%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.25,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (CV, AV, CVL))


name = '见敌必战'
skill = [Skill_112281]
