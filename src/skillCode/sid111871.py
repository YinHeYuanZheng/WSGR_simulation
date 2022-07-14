# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 安东尼奥·达诺利

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""灵活作战(3级)：队伍平均索敌值低于敌方时提升自身30点回避值，降低2点命中值；队伍平均索敌值高于敌方时提升自身30%暴击率。
"""


class Skill_111871_1(Skill):
    """队伍平均索敌值低于敌方时提升自身30点回避值，降低2点命中值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-2,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return enemy.get_avg_status('recon') < \
            friend.get_avg_status('recon')


class Skill_111871_2(Skill):
    """队伍平均索敌值高于敌方时提升自身30%暴击率"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return enemy.get_avg_status('recon') > \
            friend.get_avg_status('recon')
