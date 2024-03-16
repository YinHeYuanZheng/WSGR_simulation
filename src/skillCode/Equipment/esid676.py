# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 鹰击反舰导弹

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_676(EquipSkill):
    """增加10%护甲穿透（同类效果只生效一个）
    C国舰船装备时提高5%伤害和10%暴击率"""
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
                    effect_type=676.1,
                    name='final_damage_buff',
                    phase=AllPhase,
                    value=0.05,
                    bias_or_weight=2
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=676.2,
                    name='crit',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                ),
            ])


skill = [Eskill_676]
