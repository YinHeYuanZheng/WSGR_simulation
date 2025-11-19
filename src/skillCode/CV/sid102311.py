# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 伦道夫-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队埃塞克斯级航母舰载机威力提升8%，航空战阶段全队U国航母、轻母暴击伤害提升15%。"""


class Skill_102311_1(Skill):
    """全队埃塞克斯级航母舰载机威力提升8%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='essex')
        self.buff = [
            CoeffBuff(
                timer=self.timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.08,
                bias_or_weight=2
            )
        ]


class Skill_102311_2(Skill):
    """航空战阶段全队U国航母、轻母暴击伤害提升15%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[CountryTarget(side=1, country='U'),
                         TypeTarget(side=1, shiptype=(CV, CVL))]
        )
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AirPhase,
                value=0.15,
                bias_or_weight=0
            ),
        ]


name = '高强度弹射'
skill = [Skill_102311_1, Skill_102311_2]
