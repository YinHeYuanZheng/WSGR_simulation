# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 鞑靼人导弹(I)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""不惧装备时增加25%攻击威力"""


class Eskill_654(EquipSkill):
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10559', '11559']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=654,
                    name='power_buff',
                    phase=AllPhase,
                    value=0.25,
                    bias_or_weight=2
                )
            ]


skill = [Eskill_654]
