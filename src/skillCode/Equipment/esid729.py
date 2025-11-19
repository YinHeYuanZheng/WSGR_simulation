# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 海鹰-1甲反舰导弹

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_729(EquipSkill):
    """增加10%护甲穿透(同类弹药效果只生效一个)，南京装备时增加5%护甲穿透"""
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
        if master.cid in ['10617', '11617']:
            self.buff.extend([
                EquipEffect(
                    timer=timer,
                    effect_type=729,
                    name='pierce_coef',
                    phase=AllPhase,
                    value=0.05,
                    bias_or_weight=0
                ),
            ])


skill = [Eskill_729]
