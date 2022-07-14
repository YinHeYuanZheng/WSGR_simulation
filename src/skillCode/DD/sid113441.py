# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 忠武

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""舰队屏护(3级)：增加自身20点反潜值、12点命中值。
昼战阶段降低敌方队伍内小、中型船15点命中值。"""


class Skill_113441_1(CommonSkill):
    """增加自身20点反潜值、12点命中值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='antisub',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


class Skill_113441_2(Skill):
    """昼战阶段降低敌方队伍内小、中型船15点命中值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(SmallShip, MidShip))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=DaytimePhase,
                value=-15,
                bias_or_weight=0
            )
        ]


name = '舰队屏护'
skill = [Skill_113441_1, Skill_113441_2]
