# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 蒙巴顿粉

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_427(EquipSkill):
    """凯利装备时增加10%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10414', '11414']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=427,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_427]
