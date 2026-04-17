# -*- coding:utf-8 -*-
# Author:昆西Alter
# env:py38
# “海标枪”导弹发射器

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_754(EquipSkill):
    """考文垂装备时增加10%暴击率和回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10640', '11640']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=754.1,
                    name='crit',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=754.2,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                ),
            ]


skill = [Eskill_754]
