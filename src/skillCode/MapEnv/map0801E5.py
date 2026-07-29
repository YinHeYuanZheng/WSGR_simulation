# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-1E点选项5(右下)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0801E5_1(PrepSkill):
    """U国舰船火力+15，装甲-10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CountryTarget(side=1, country='U')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            ),
        ]


name = '8-1E点选项5(右下)'
effect = 'U国舰船火力+15，装甲-10'
skill = [NormalMap_0801E5_1]
