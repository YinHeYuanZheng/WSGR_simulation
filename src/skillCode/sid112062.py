# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 北卡罗来纳-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""威慑(3级)：提升自身火力值10点，降低自身闪避值5点，
降低敌方战列和战巡的火力值10点、闪避值10点（对敌方旗舰无效）。
"""


class Skill_112062_1(CommonSkill):
    """提升自身火力值10点，降低自身闪避值5点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                value=10,
                phase=AllPhase,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='evasion',
                value=-5,
                phase=AllPhase,
                bias_or_weight=0
            )
        ]


class Skill_112062_2(Skill):
    """降低敌方战列和战巡的火力值10点、闪避值10点（对敌方旗舰无效）"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(BB, BC))

        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                value=-10,
                phase=AllPhase,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                value=-10,
                phase=AllPhase,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            if tmp_target.loc != 1:
                for tmp_buff in self.buff[:]:
                    tmp_target.add_buff(tmp_buff)


skill = [Skill_112062_1, Skill_112062_2]
