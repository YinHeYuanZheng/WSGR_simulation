# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 瓜达卡纳尔改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队轻母舰载机威力提高25%，命中率提高15%，在非单横阵时可以进行先制反潜。"""


class Skill_113111_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=CVL)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.25,
                bias_or_weight=2
            ),
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0
            ),
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=AntiSubPhase
            )
        ]


name = '特别鱼叉'
skill = [Skill_113111_1]
