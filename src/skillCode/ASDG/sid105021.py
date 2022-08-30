# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 济南-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加全队导驱15%护甲穿透。
增加全队C国船12点火力值、装甲值、回避值和12%暴击率。"""


class Skill_105021_1(Skill):
    """增加全队导驱15%护甲穿透。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=ASDG)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='pierce_coef',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0
            )
        ]


class Skill_105021_2(Skill):
    """增加全队C国船12点火力值、装甲值、回避值和12%暴击率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='C')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.12,
                bias_or_weight=0
            )
        ]



name = '海鹰巡弋'
skill = [Skill_105021_1, Skill_105021_2]
