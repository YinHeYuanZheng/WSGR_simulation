# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 不挠-1

from src.wsgr.equipment import *
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""持久作战(3级)：提升自身所携带的鱼雷机的鱼雷值7点。
自身血量降低时不会对自身属性造成影响，
且同时减少30%自身因战斗造成的载机量损失（大破时除外）。"""


class Skill_103191_1(CommonSkill):
    """提升自身所携带的鱼雷机的鱼雷值7点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=(DiveBomber,)
        )
        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=(AllPhase,),
                value=7,
                bias_or_weight=0
            )
        ]


class Skill_103191_2(Skill):
    """自身血量降低时不会对自身属性造成影响，
    且同时减少30%自身因战斗造成的载机量损失（大破时除外）。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=(AllPhase,),
                atk_request=[BuffRequest_1]
            ),
            AtkBuff(
                timer=timer,
                name='fall_rest',
                phase=(AirPhase,),
                value=-0.3,
                bias_or_weight=1,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.atk_body.damaged < 3


name = '持久作战'
skill = [Skill_103191_1, Skill_103191_2]
