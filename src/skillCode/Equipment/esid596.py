# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 掠夺者攻击机

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_596(EquipSkill):
    """胜利和皇家方舟(R09)装备时提高5%伤害"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10483', '11483', '10455', '11455']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=596,
                    name='final_damage_buff',
                    phase=AllPhase,
                    value=0.05,
                    bias_or_weight=2
                )
            ]


skill = [Eskill_596]
