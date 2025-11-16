# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 海雌狐FAW.2战斗机

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_601(EquipSkill):
    """胜利和皇家方舟(R09)装备时增加25制空值"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10483', '11483', '10455', '11455']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=601,
                    name='air_ctrl_buff',
                    phase=AirPhase,
                    value=25,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_601]
