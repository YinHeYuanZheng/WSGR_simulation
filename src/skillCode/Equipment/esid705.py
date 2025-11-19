# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 鹰击83反舰导弹

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_705(EquipSkill):
    """增加10%护甲穿透(同类弹药效果只生效一个)，C国舰船装备时提高20%暴击率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=3,
                name='pierce_coef',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]
        if master.status['country'] == 'C':
            self.buff.extend([
                EquipEffect(
                    timer=timer,
                    effect_type=705,
                    name='crit',
                    phase=AllPhase,
                    value=0.2,
                    bias_or_weight=0
                )
            ])


skill = [Eskill_705]
