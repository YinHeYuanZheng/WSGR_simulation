# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 海鹰反舰导弹

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_021(EquipSkill):
    """增加X1%护甲穿透(同类弹药效果只生效一个)，济南装备时提高X2%伤害"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=3,
                name='pierce_coef',
                phase=AllPhase,
                value=self.value[0],
                bias_or_weight=0
            )
        ]
        if master.cid in ['10502', '11502']:
            self.buff.append(
                EquipEffect(
                    timer=timer,
                    effect_type=21,
                    name='final_damage_buff',
                    phase=AllPhase,
                    value=self.value[1],
                    bias_or_weight=2
                )
            )


skill = [Eskill_021]
