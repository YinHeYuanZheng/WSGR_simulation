# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# M-296

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""回避值增加25点，被暴击率提升10%。
(Lv.3)攻击力不会因为自身补给损失而降低。"""


class Skill_115301_1(CommonSkill):
    """回避值增加25点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            )
        ]


class Skill_115301_2(Skill):
    """被暴击率提升10%。攻击力不会因为自身补给损失而降低"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='be_crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_supply',
                phase=AllPhase
            )
        ]


name = 'AIP'
skill = [Skill_115301_1, Skill_115301_2]
