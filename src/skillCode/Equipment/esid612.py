# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# П-35反舰导弹

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_612(EquipSkill):
    """增加10%护甲穿透(同类弹药效果只生效一个)，格罗兹尼装备时额外提高5%护甲穿透"""
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
        if master.cid in ['10533', '11533']:
            self.buff.append(
                EquipEffect(
                    timer=timer,
                    effect_type=612,
                    name='pierce_coef',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                )
            )


skill = [Eskill_612]
