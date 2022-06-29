# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 袖珍舰载艇

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_019(EquipSkill):
    """IIIA装备时提高X1%伤害和X2%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10518', '11518']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=19.1,
                    name='final_damage_buff',
                    phase=AllPhase,
                    value=self.value[0],
                    bias_or_weight=2
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=19.2,
                    name='hit_rate',
                    phase=AllPhase,
                    value=self.value[1],
                    bias_or_weight=0
                )
            ]


skill = [Eskill_019]
