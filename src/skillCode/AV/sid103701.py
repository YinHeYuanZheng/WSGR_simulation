# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 光辉-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_103701(Skill):
    """先驱首战(3级)：提升相邻上下航母，装母，轻母15点命中值和20%炮击战威力。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='near',
            shiptype=(CV, CVL, AV)
        )

        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=ShellingPhase,
                value=0.2,
                bias_or_weight=2
            )
        ]


name = '先驱首战'
skill = [Skill_103701]
