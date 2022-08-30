# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 兴登堡-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_102001(Skill):
    """当自身不处于中破、大破状态时，炮击战自身攻击时降低敌方装甲15%，并附带固定伤害20点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name="ignore_armor",
                phase=ShellingPhase,
                value=-0.15,
                bias_or_weight=1,
                atk_request=[BuffRequest_1]
            ),
            AtkBuff(
                timer=timer,
                name="extra_damage",
                phase=ShellingPhase,
                value=20,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.atk_body.damaged == 1


skill = [Skill_102001]
