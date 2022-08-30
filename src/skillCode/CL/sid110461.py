# -*- coding: utf-8 -*-
# Author:银河远征
# env:py38
# 夕张改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""实验平台(3级)：自身携带的装备获得160%的基础性能。"""


class Skill_110461(CommonSkill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master)
        )
        self.buff = [
            CommonBuff(
                timer=timer,
                name='all_status',
                phase=AllPhase,
                value=0.6,
                bias_or_weight=1
            )
        ]


name = '实验平台'
skill = [Skill_110461]
