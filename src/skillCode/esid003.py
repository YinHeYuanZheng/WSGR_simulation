# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 装备穿甲特效

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Eskill_003(EquipSkill):
    """增加X%护甲穿透（同类弹药效果只生效一个）"""
    def __init__(self, timer, master, value):
        super().__init__(timer, master, value)
        self.target = SelfTarget(master)
        self.buff = [
            EquipEffect(
                timer=timer,
                effect_type=3,
                name='pierce_coef',
                phase=(AllPhase,),
                value=self.value[0],
                bias_or_weight=0
            )
        ]


skill = [Eskill_003]
