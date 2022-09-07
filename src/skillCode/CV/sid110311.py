# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 大黄蜂改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110311_1(Skill):
    """自身航空战阶段自身攻击命中后必定暴击
    炮击战阶段自身伤害降低10%
    炮击战阶段,优先攻击要塞、机场、港口、航母
    自身全阶段攻击要塞、机场、港口、航母时降低敌方100%对空值（不包括装备）"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='must_crit',
                phase=AirPhase,
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=-0.1
            ),
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=ShellingPhase,
                target=TypeTarget(side=0,
                                  shiptype=(Fortness, Airfield, Port, CV)),
                ordered=False
            ),
            AtkBuff(
                timer=timer,
                name='ignore_antiair',
                phase=AllPhase,
                value=-1,
                bias_or_weight=1,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target,
                          (Fortness, Airfield, Port, CV))


class Skill_110311_2(Skill):
    """当队伍中航母≥2时，增加自身30%暴击伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        number = len(
            TypeTarget(
                side=1,
                shiptype=CV
            ).get_target(friend, enemy)
        )
        return number >= 2


name = '远洋破袭'
skill = [Skill_110311_1, Skill_110311_2]
