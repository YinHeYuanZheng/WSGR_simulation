# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 袖珍舰载艇

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_593(EquipSkill):
    """IIIA装备时提高15%伤害和5%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10518', '11518']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=593.1,
                    name='final_damage_buff',
                    phase=AllPhase,
                    value=0.15,
                    bias_or_weight=2
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=593.2,
                    name='hit_rate',
                    phase=AllPhase,
                    value=0.05,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_593]
