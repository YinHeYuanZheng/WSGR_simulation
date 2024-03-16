# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 红旗61防空导弹

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_670(EquipSkill):
    """鹰潭装备时增加25%伤害"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10287', '11287']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=670,
                    name='final_damage_buff',
                    phase=AllPhase,
                    value=0.25,
                    bias_or_weight=2
                )
            ]


skill = [Eskill_670]
