# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 史密斯改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""当编队中存在大型船时，自身回避值增加12点，航空战阶段增加自身40%被攻击概率。
当编队中不存在大型船时，自身攻击威力提升15%，昼战阶段免疫受到的第一次攻击"""


class Skill_114251_1(Skill):
    """当编队中存在大型船时，自身回避值增加12点，航空战阶段增加自身40%被攻击概率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            MagnetBuff(
                timer=timer,
                phase=AirPhase,
                rate=0.4
            )
        ]

    def is_active(self, friend, enemy):
        num_large = len(TypeTarget(side=1, shiptype=LargeShip).get_target(friend, enemy))
        return num_large


class Skill_114251_2(Skill):
    """当编队中不存在大型船时，自身攻击威力提升15%，昼战阶段免疫受到的第一次攻击"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='power_buff',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=2
            ),
            SpecialBuff(
                timer=timer,
                name='shield',
                phase=DaytimePhase,
                exhaust=1
            )
        ]

    def is_active(self, friend, enemy):
        num_large = len(TypeTarget(side=1, shiptype=LargeShip).get_target(friend, enemy))
        return num_large == 0


name = '幸运水花'
skill = [Skill_114251_1, Skill_114251_2]
