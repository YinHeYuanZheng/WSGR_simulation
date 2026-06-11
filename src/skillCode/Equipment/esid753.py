# -*- coding:utf-8 -*-
# Author:昆西Alter
# env:py38
# “海标枪”GWS30导弹

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_753(EquipSkill):
    """考文垂装备时额外增加15%护甲穿透"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10640', '11640']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=753,
                    name='pierce_coef',
                    phase=AllPhase,
                    value=0.15,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_753]
