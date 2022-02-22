# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 不挠-1

from ..wsgr.equipment import DiveBomber
from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

"""持久作战(3级)：提升自身所携带的鱼雷机的鱼雷值7点。
自身血量降低时不会对自身属性造成影响，
且同时减少30%自身因战斗造成的载机量损失（大破时除外）。"""


class Skill_103191_1(CommonSkill):
    """提升自身所携带的鱼雷机的鱼雷值7点"""

    def __init__(self, master):
        super().__init__(master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=(DiveBomber,)
        )
        self.buff = [
            CommonBuff(
                name='torpedo',
                phase=(AllPhase,),
                value=7,
                bias_or_weight=0
            )
        ]


class Skill_103191_2(Skill):
    """自身血量降低时不会对自身属性造成影响，"""

    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        # self.buff = [SpecialBuff(
        #     name='ignore_dmg',
        #     phase=(AllPhase, ),
        #     bias_or_weight=0
        # )]


# todo 且同时减少30%自身因战斗造成的载机量损失（大破时除外）。


skill = [Skill_103191_1]
