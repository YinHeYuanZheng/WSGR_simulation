# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# G15-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身火力值15点、航速3节。
航空战阶段自身被攻击概率提高40%，受到伤害减少15点。"""


class Skill_104861_1(CommonSkill):
    """增加自身火力值15点、航速3节。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0,
            ),
            CommonBuff(
                timer=timer,
                name='speed',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            )
        ]


class Skill_104861_2(Skill):
    """航空战阶段自身被攻击概率提高40%，受到伤害减少15点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=(AirPhase,),
                rate=0.4
            ),
            CoeffBuff(
                timer=timer,
                name='reduce_damage',
                phase=(AirPhase,),
                value=15,
                bias_or_weight=0
            )
        ]


name = '飞石战法'
skill = [Skill_104861_1, Skill_104861_2]
