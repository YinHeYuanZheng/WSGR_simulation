# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 瑞鹤改-1

import numpy as np
import random
from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

"""幸运的云雨区(3级)：自身幸运值提升15，被攻击时，最大增加80%幸运值的装甲，最大增加80%幸运值的回避。"""


class Skill_112191_1(CommonSkill):
    """自身幸运值提升15"""

    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                name='luck',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_112191_2(Skill):
    """最大增加80%幸运值的装甲，最大增加80%幸运值的回避"""

    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            LuckBuff(
                name='armor',
                bias_or_weight=0
            ),
            LuckBuff(
                name='evasion',
                bias_or_weight=0
            )
        ]


class LuckBuff(StatusBuff):
    def __init__(self, name, bias_or_weight):
        super().__init__(name=name,
                         phase=AllPhase,
                         value=1,
                         bias_or_weight=bias_or_weight)

    def is_active(self, *args, **kwargs):
        """因为每次都会判断is_active，因此利用该函数生成每次不同的值"""
        self.value = np.ceil(
            (1 - random.random()) * 0.8
            * self.master.get_final_status('luck')
        )
        return True


skill = [Skill_112191_1, Skill_112191_2]
