# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 勇猛-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队U国舰船对敌方大型船造成的伤害提高15%。
自身为旗舰时，航空战阶段提升全队航母、装母、轻母7%的舰载机威力。"""


class Skill_105131_1(Skill):
    """全队U国舰船对敌方大型船造成的伤害提高15%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='U')
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.15,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, LargeShip)


class Skill_105131_2(Skill):
    """自身为旗舰时，航空战阶段提升全队航母、装母、轻母7%的舰载机威力。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(CV, AV, CVL))
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AirPhase,
                value=0.07,
                bias_or_weight=1
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


skill = [Skill_105131_1, Skill_105131_2]
