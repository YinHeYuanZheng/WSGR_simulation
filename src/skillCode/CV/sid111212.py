# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 企业改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身攻击必中，幸运、回避和火力增加15点，舰载机威力、暴击率和暴击伤害提高30%。
炮击战阶段自身优先攻击敌方耐久值最高的单位，被命中过的单位装甲值、回避值降低30点，无法行动。"""


class Skill_111212_1(CommonSkill):
    """幸运、回避和火力增加15点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CommonBuff(
                timer=timer,
                name='luck',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_111212_2(Skill):
    """自身攻击必中，舰载机威力、暴击率和暴击伤害提高30%。
    炮击战阶段自身优先攻击敌方耐久值最高的单位，被命中过的单位装甲值、回避值降低30点，无法行动。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            SpecialBuff(
                timer=timer,
                name='must_hit',
                phase=AllPhase
            ),
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=2
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0
            ),
            PriorTargetBuff(
                timer=timer,
                name='prior_loc_target',
                phase=ShellingPhase,
                target=HighestTarget(side=0),
                ordered=True
            ),
            AtkHitBuff(
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
                    ),
                    StatusBuff(
                        timer=timer,
                        name='evasion',
                        phase=AllPhase,
                        value=-30,
                        bias_or_weight=0
                    ),
                    ActPhaseBuff(
                        timer=timer,
                        name='not_act_phase',
                        phase=AllPhase
                    )
                ],
                side=0
            )
        ]


class HighestTarget(Target):
    def get_target(self, friend, enemy):
        fleet = self.get_target_fleet(friend, enemy)
        fleet.sort(key=lambda x: -x.status['health'])
        return fleet


name = '大E'
skill = [Skill_111212_1, Skill_111212_2]
