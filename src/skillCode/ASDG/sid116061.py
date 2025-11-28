# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 汉堡改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队G国小型船索敌值增加4点，火力值、装甲值和命中值增加12点。
自身昼战阶段伤害提高25%，被自身命中的单位回避值和命中值降低40点。"""


class Skill_116061_1(PrepSkill):
    """全队G国小型船索敌值增加4点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[TypeTarget(side=1, shiptype=SmallShip),
                         CountryTarget(side=1, country='G')]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            )
        ]


class Skill_116061_2(Skill):
    """全队G国小型船火力值、装甲值和命中值增加12点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[TypeTarget(side=1, shiptype=SmallShip),
                         CountryTarget(side=1, country='G')]
        )
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
                name='accuracy',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


class Skill_116061_3(Skill):
    """自身昼战阶段伤害提高25%，被自身命中的单位回避值和命中值降低40点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=DaytimePhase,
                value=0.25
            ),
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=DaytimePhase,
                buff=[
                    StatusBuff(
                        timer=timer,
                        name='evasion',
                        phase=AllPhase,
                        value=-40,
                        bias_or_weight=0
                    ),
                    StatusBuff(
                        timer=timer,
                        name='accuracy',
                        phase=AllPhase,
                        value=-40,
                        bias_or_weight=0
                    )
                ],
                side=0
            )
        ]


name = '锐卫'
skill = [Skill_116061_1, Skill_116061_2, Skill_116061_3]
