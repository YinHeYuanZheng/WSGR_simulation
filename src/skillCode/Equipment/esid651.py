# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 方位盘（A150）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加15%护甲穿透（同类弹药效果只生效一个）。A150装备时增加10%攻击力与5%命中率"""


class Eskill_651_1(EquipSkill):
    """增加15%护甲穿透（同类弹药效果只生效一个）"""
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


class Eskill_651_2(EquipSkill):
    """A150装备时增加10%攻击力与5%命中率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10191', '11191']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=651.1,
                    name='power_buff',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=2
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=651.2,
                    name='hit_rate',
                    phase=AllPhase,
                    value=0.05,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_651_1, Eskill_651_2]
