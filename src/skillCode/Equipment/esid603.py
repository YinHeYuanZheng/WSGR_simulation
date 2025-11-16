# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# F6F地狱猫战斗机(麦坎贝尔)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_603(EquipSkill):
    """埃塞克斯装备时航空战阶段增加15%攻击威力和增加20制空值"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = []
        if master.cid in ['10226', '11226']:
            self.buff = [
                EquipEffect(
                    timer=timer,
                    effect_type=603.1,
                    name='air_atk_buff',
                    phase=AirPhase,
                    value=0.15,
                    bias_or_weight=2
                ),
                EquipEffect(
                    timer=timer,
                    effect_type=603.2,
                    name='air_ctrl_buff',
                    phase=AirPhase,
                    value=20,
                    bias_or_weight=0
                )
            ]


skill = [Eskill_603]
