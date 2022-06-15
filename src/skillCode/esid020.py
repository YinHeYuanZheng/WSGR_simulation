# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 海鹰导弹发射器

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_020(EquipSkill):
    """济南装备时提高X%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10502', '11502']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=20,
                    name='miss_rate',
                    phase=AllPhase,
                    value=self.value[0],
                    bias_or_weight=0
                )
            ]


skill = [Eskill_020]
