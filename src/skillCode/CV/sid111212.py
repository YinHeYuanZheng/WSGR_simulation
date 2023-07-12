# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 企业改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_111212_1(CommonSkill):
    """增加自身闪避值10点、火力值15点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=(AllPhase,),
                value=10,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='fire',
                phase=(AllPhase,),
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_111212_2(Skill):
    """增加自身暴击率20%，首轮炮击必中
    炮击战阶段，优先攻击敌方耐久值最高的单位，被命中的单位降低装甲值10点与火力值10点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=(AllPhase,),
                value=0.20,
                bias_or_weight=0
            ),
            SpecialBuff(
                timer=timer,
                name='must_hit',
                phase=FirstShellingPhase
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
                        name='fire',
                        phase=(AllPhase,),
                        value=10,
                        bias_or_weight=0
                    ),
                    StatusBuff(
                        timer=timer,
                        name='armor',
                        phase=(AllPhase,),
                        value=15,
                        bias_or_weight=0
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
