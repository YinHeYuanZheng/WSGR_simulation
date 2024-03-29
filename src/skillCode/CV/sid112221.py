# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 苍龙改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110231(Skill):
    """增加自身暴击率10%，被暴击率5%，自身攻击附带25%护甲穿透效果（不能和装备叠加）。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.10,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='be_crit',
                phase=AllPhase,
                value=0.05,
                bias_or_weight=0
            ),
            UniqueEffect(
                timer=timer,
                effect_type=3,
                name='pierce_coef',
                phase=AllPhase,
                value=0.25,
                bias_or_weight=0
            )
        ]


name = '舰爆出击'
skill = [Skill_110231]
