# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# “白蛉”反舰导弹

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_751(EquipSkill):
    """增加15%护甲穿透(同类弹药效果只生效一个)，S国舰船装备时战斗中额外增加5%护甲穿透"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=3,
                name='pierce_coef',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0
            )
        ]
        if master.status['country'] == 'S':
            self.buff.append(
                EquipEffect(
                    timer=timer,
                    effect_type=751,
                    name='pierce_coef',
                    phase=AllPhase,
                    value=0.05,
                    bias_or_weight=0
                )
            )


skill = [Eskill_751]
