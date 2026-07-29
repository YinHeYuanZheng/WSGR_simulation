# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-3H点选项3(中间)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_0803H3_1(PrepSkill):
    """主力舰火力-15，装甲、回避+10"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=MainShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
        ]


name = '8-3H点选项3(中间)'
effect = '主力舰火力-15，装甲、回避+10'
skill = [NormalMap_0803H3_1]
