# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# P-35反舰导弹（1134）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_692(EquipSkill):
    """增加10%护甲穿透(同类弹药效果只生效一个)，塞瓦斯托波尔装备时额外提高5%护甲穿透"""
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
        if master.cid in ['10581', '11581']:
            self.buff.append(
                EquipEffect(
                    timer=timer,
                    effect_type=692,
                    name='pierce_coef',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                )
            )


skill = [Eskill_692]
