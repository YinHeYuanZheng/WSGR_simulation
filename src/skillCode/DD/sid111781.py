# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 沙利文

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""战斗中，自身火力、装甲-10、回避-5，
旗舰对空、装甲+30、回避+15。(自身旗舰无效)"""


class Skill_111781_1(Skill):
    """战斗中，自身火力、装甲 -10、回避-5，(自身旗舰无效)"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            ),
        ]
    
    def is_active(self, friend, enemy):
        return self.master.loc != 1


class Skill_111781_2(Skill):
    """旗舰对空、装甲+30、回避+15。(自身旗舰无效)"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=1, loc=[1])
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
        ]

    def is_active(self, friend, enemy):
        return self.master.loc != 1


name = '守护英雄之人'
skill = [Skill_111781_1, Skill_111781_2]
