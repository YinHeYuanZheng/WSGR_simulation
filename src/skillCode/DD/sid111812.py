# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 威廉·D·波特

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""提升自身对空和装甲30点，提升自己在炮击战阶段被航母、装母和轻母攻击概率40%。"""


class Skill_111812_1(CommonSkill):
    """提升自身对空和装甲30点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            )
        ]


class Skill_111812_2(Skill):
    """提升自己在炮击战阶段被航母、装母和轻母攻击概率40%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=.4,
                atk_request=[ATKRequest_1],
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.atk_body, (CV, CVL, AV))


name = '幸运的威利'
skill = [Skill_111812_1, Skill_111812_2]
