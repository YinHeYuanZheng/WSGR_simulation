# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# FJ-4B（16）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""埃塞克斯级航母装备时增加5%伤害"""


class Eskill_653(EquipSkill):
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.status['tag'] == 'essex':
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=653,
                    name='final_damage_buff',
                    phase=AllPhase,
                    value=0.05,
                    bias_or_weight=2
                )
            ]


skill = [Eskill_653]
