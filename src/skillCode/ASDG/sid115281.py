# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 芝加哥改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加全队中型船12点装甲值，
增加全队护卫舰30点对空值和12点回避值。
全队航空战阶段受到的伤害降低50%。"""


class Skill_115281_1(Skill):
    """增加全队中型船12点装甲值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=MidShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


class Skill_115281_2(Skill):
    """增加全队护卫舰30点对空值和12点回避值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=CoverShip)
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
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


class Skill_115281_3(Skill):
    """全队航空战阶段受到的伤害降低50%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AirPhase,
                value=-0.5
            )
        ]


name = '天穹守护'
skill = [Skill_115281_1, Skill_115281_2, Skill_115281_3]
