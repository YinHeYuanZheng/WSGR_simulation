# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# СМ-70旋转发射器

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_613(EquipSkill):
    """格罗兹尼装备时提高10%回避率"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10533', '11533']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=613,
                    name='miss_rate',
                    phase=AllPhase,
                    value=0.1,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_613]
