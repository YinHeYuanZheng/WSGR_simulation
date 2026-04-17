# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# PAT-52火箭鱼雷

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import *


class Eskill_248(EquipSkill):
    """航空战阶段增加10%鱼雷机命中率，炮击战阶段增加5%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='hit_rate',
                phase=AirPhase,
                value=0.1,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            ),
            EquipEffect(
                timer=timer,
                effect_type=248,
                name='hit_rate',
                phase=ShellingPhase,
                value=0.03,
                bias_or_weight=0
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, AirDiveAtk)


skill = [Eskill_248]
