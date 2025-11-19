# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 马舒卡导弹MK2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_631(EquipSkill):
    """絮弗伦装备时增加20%伤害"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10552', '11552']:
            self.buff.append(
                EquipEffect(
                    timer=timer,
                    effect_type=631,
                    name='final_damage_buff',
                    phase=AllPhase,
                    value=0.2,
                    bias_or_weight=2
                )
            )


skill = [Eskill_631]


