# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 摩尔曼斯克改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""航线援护(3级)：提升上方所有单位6点装甲值和自身5点对空与火力值，
炮击战阶段优先攻击轻巡、驱逐。"""


class Skill_111601_1(Skill):
    """提升上方所有单位6点装甲值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=6,
            direction='up'
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            )
        ]


class Skill_111601_2(Skill):
    """提升自身5点对空与火力值，炮击战阶段优先攻击位置排在前方的敌方轻巡、驱逐。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=ShellingPhase,
                target=TypeTarget(side=0, shiptype=(CL, DD)),
                ordered=True
            )
        ]


skill = [Skill_111601_1, Skill_111601_2]
