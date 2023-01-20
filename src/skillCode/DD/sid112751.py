# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 康弗斯改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身攻击威力不会因耐久损伤而降低。
编队里“小海狸中队”的舰船战斗时增加12点鱼雷值、命中值、回避值和装甲值，提升12%暴击率。"""


class Skill_112751_1(Skill):
    """自身攻击威力不会因耐久损伤而降低。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase
            )
        ]


class Skill_112751_2(Skill):
    """编队里“小海狸中队”的舰船战斗时增加12点鱼雷值、命中值、回避值和装甲值，提升12%暴击率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='little_beavers')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
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
            StatusBuff(
                timer=timer,
                name='armor',
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
            ),
        ]


name = '31节中队'
skill = [Skill_112751_1, Skill_112751_2]
