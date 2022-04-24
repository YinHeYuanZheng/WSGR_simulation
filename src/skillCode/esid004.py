# -*- coding: utf-8 -*-
# Author:银河远征
# env:py38
# 超重弹特效

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_004(EquipSkill):
    """炮击战阶段增加X%攻击上限（同类弹药效果只生效一个）"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=4,
                name='uplimit_buff',
                phase=ShellingPhase,
                value=self.value[0],
                bias_or_weight=0
            )
        ]


skill = [Eskill_004]
