# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# Kw45-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身优先攻击敌方航速最低的单位，攻击航速低于自身的敌人时，火力值增加30点，造成的伤害提高30%。"""


class Skill_106311_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_loc_target',
                phase=AllPhase,
                target=LowestSpeedTarget(side=0),
                ordered=True
            ),
            AtkBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=30,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.3,
                atk_request=[BuffRequest_1],
            ),
        ]


class LowestSpeedTarget(Target):
    """返回敌方按速度升序排列的目标列表"""
    def get_target(self, friend, enemy):
        fleet = self.get_target_fleet(friend, enemy)
        fleet.sort(key=lambda x: x.get_final_status('speed'))
        return fleet


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.get_final_status('speed') < \
               self.atk.source.get_final_status('speed')


name = '急速'
skill = [Skill_106311_1]
