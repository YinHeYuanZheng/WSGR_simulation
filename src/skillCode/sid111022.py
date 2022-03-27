# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 陆奥-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
"""	增加自身25%暴击率和50%被暴击率。炮击战阶段攻击战列舰时无视目标护甲。"""


class Skill_111022_1(Skill):
    """增加自身25%暴击率和50%被暴击率。"""
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
            ),
            CoeffBuff(
                timer=timer,
                name='be_crit',
                phase=AllPhase,
                value=0.5,
                bias_or_weight=0
            )
        ]


class Skill_111022_2(Skill):
    """炮击战阶段攻击战列舰时无视目标护甲。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='ignore_armor',
                phase=ShellingPhase,
                value=1,
                bias_or_weight=1,
                atk_request=[Request_1]
            )
        ]


class Request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, BB)


skill = [Skill_111022_1]
