# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# MK13发射系统(I)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""不惧装备时增加10%暴击率和10%回避率"""


class Eskill_655(EquipSkill):
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10559', '11559']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=655.1,
                    name='crit',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=655.2,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                ),
            ]


skill = [Eskill_655]
