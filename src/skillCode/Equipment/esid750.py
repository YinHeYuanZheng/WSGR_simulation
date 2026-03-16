# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# TBF(VT-8)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_750(EquipSkill):
    """航空战阶段增加8%鱼雷机攻击威力，萨拉托加装备时额外增加12%攻击威力"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=750.1,
                name='air_dive_atk_buff',
                phase=AirPhase,
                value=0.08,
                bias_or_weight=2
            )
        ]
        if master.cid in ['10030', '11030']:
            self.buff.append(
                EquipEffect(
                    timer=timer,
                    effect_type=750.2,
                    name='power_buff',
                    phase=AllPhase,
                    value=0.12,
                    bias_or_weight=2
                )
            )


skill = [Eskill_750]
