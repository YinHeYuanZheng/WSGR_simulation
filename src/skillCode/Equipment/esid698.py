# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# MK143战斧导弹发射箱（91）

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_698(EquipSkill):
    """密苏里装备时增加15%暴击率，炮击战阶段增加10%攻击威力"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10209', '11209']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=698.1,
                    name='crit',
                    phase=AllPhase,
                    value=0.15,
                    bias_or_weight=0
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=698.2,
                    name='power_buff',
                    phase=ShellingPhase,
                    value=0.1,
                    bias_or_weight=2
                )
            ]


skill = [Eskill_698]
