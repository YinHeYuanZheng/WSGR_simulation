# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# U-2540

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队G国潜艇航速提升3节、回避值增加9点、
战斗结算获得的经验提高20%。"""


class Skill_112911_1(PrepSkill):
    """全队G国潜艇航速提升3节"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[CountryTarget(side=1, country='G'),
                         TypeTarget(side=1, shiptype=SS)]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='speed',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            )
        ]


class Skill_112911_2(Skill):
    """全队G国潜艇回避值增加9点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[CountryTarget(side=1, country='G'),
                         TypeTarget(side=1, shiptype=SS)]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]


name = '次世代潜艇'
skill = [Skill_112911_1, Skill_112911_2]
