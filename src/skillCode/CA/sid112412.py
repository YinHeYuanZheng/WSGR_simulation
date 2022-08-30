# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 巴尔的摩改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""集中火力(3级)：作为旗舰时，降低全队10点装甲值，提升全队20点火力值。
自身炮击战命中航母，装母以外单位时有50%概率造成1.5倍伤害，被技能命中后的目标会降低30点装甲值。"""


class Skill_112412_1(Skill):
    """作为旗舰时，降低全队10点装甲值，提升全队20点火力值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


class Skill_112412_2(Skill):
    """自身炮击战命中航母，装母以外单位时有50%概率造成1.5倍伤害，
    被技能命中后的目标会降低30点装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='give_atk',
                phase=ShellingPhase,
                buff=[
                    DuringAtkBuff(
                        timer=timer,
                        name='final_damage_buff',
                        phase=ShellingPhase,
                        value=0.5,
                        bias_or_weight=2
                    ),
                    Dur_AtkHitBuff(
                        timer=timer,
                        name='atk_hit',
                        phase=ShellingPhase,
                        buff=[
                            StatusBuff(
                                timer=timer,
                                name='armor',
                                phase=AllPhase,
                                value=-30,
                                bias_or_weight=0
                            )
                        ],
                        side=0
                    )
                ],
                side=1,
                atk_request=[ATKRequest_1],
                rate=0.5
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return not isinstance(self.atk.target, (CV, AV))


class Dur_AtkHitBuff(AtkHitBuff):
    def is_during_buff(self):
        return True


name = '集中火力'
skill = [Skill_112412_1, Skill_112412_2]
