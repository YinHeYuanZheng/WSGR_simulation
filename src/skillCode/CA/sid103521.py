# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 莫斯科-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""巡洋舰压制(3级)：提升自身在内全队轻巡和重巡的回避7点，提升全队所有轻巡的火力7点。
梯形阵时增加莫斯科自身暴击和被暴击各10点"""


class Skill_103521_1(Skill):
    """提升自身在内全队轻巡和重巡的回避7点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(CL, CA))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=7,
                bias_or_weight=0
            )
        ]


class Skill_103521_2(Skill):
    """提升全队所有轻巡的火力7点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=CL)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=7,
                bias_or_weight=0
            )
        ]


class Skill_103521_3(Skill):
    """梯形阵时增加莫斯科自身暴击和被暴击各10点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='be_crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 4


name = '巡洋舰压制'
skill = [Skill_103521_1, Skill_103521_2, Skill_103521_3]
