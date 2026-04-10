# -*- coding:utf-8 -*-
# Author:zzhh225
# Edited by: 银河远征(20260410)
# env:py38
# 齐柏林伯爵改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""斯图卡(3级)：当队伍中战列≥2时，全队战列火力值和命中值增加12点，暴击率提高12%；
当队伍中战列≤2时，自身装甲值和回避值增加25点，舰载机威力和暴击率提高25%。
炮击战阶段自身优先攻击敌方火力值最高的单位，被命中过的单位无法行动。
"""


class Skill_111181_1(Skill):
    """当队伍中战列≥2时，全队战列火力值和命中值增加12点，暴击率提高12%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=BB)
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
                name='accuracy',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.12,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        number = len(
            TypeTarget(
                side=1,
                shiptype=BB
            ).get_target(friend, enemy)
        )
        return number >= 2


class Skill_111181_2(Skill):
    """当队伍中战列≤2时，自身装甲值和回避值增加25点，舰载机威力和暴击率提高25%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.25,
                bias_or_weight=2
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.25,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        number = len(
            TypeTarget(
                side=1,
                shiptype=BB
            ).get_target(friend, enemy)
        )
        return number <= 2


class Skill_111181_3(Skill):
    """炮击战阶段自身优先攻击敌方火力值最高的单位，被命中过的单位无法行动"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_loc_target',
                phase=ShellingPhase,
                target=HighestFireTarget(side=0),
                ordered=True
            ),
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=ShellingPhase,
                buff=[
                    ActPhaseBuff(
                        timer=timer,
                        name='not_act_phase',
                        phase=AllPhase
                    )
                ],
                side=0
            )
        ]


class HighestFireTarget(Target):
    """返回敌方按火力值降序排列的目标列表"""
    def get_target(self, friend, enemy):
        fleet = self.get_target_fleet(friend, enemy)
        fleet.sort(key=lambda x: -x.get_final_status('fire'))
        return fleet


name = '斯图卡'
skill = [Skill_111181_1, Skill_111181_2, Skill_111181_3]
