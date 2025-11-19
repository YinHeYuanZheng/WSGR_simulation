# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 马耳他-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队E国装母、航母、轻母舰载机威力提升10%。
当全队装母>=3时，全队E国舰船命中率提高15%，暴击伤害增加20%。
当全队航母>=3时，全队E国装母攻击时提升其自身50%火力值的额外伤害。"""


class Skill_103001_1(Skill):
    """全队E国装母、航母、轻母舰载机威力提升10%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                CountryTarget(side=1, country='E'),
                TypeTarget(side=1, shiptype=(AV, CV, CVL))
            ]
        )
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=2
            )
        ]


class Skill_103001_2(Skill):
    """当全队装母>=3时，全队E国舰船命中率提高15%，暴击伤害增加20%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='E')
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=.15,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=.2,
                bias_or_weight=0
            ),
        ]

    def is_active(self, friend, enemy):
        av = TypeTarget(side=1, shiptype=AV).get_target(friend, enemy)
        return len(av) >= 3


class Skill_103001_3(Skill):
    """当全队航母>=3时，全队E国装母攻击时提升其自身50%火力值的额外伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                CountryTarget(side=1, country='E'),
                TypeTarget(side=1, shiptype=AV)
            ]
        )
        self.buff = [
            FireExtraDamage(
                timer=timer,
                name='extra_damage',
                phase=AllPhase,
                value=0.5,
                bias_or_weight=0
            ),
        ]

    def is_active(self, friend, enemy):
        cv = TypeTarget(side=1, shiptype=CV).get_target(friend, enemy)
        return len(cv) >= 3


class FireExtraDamage(CoeffBuff):
    def change_value(self, *args, **kwargs):
        self.value = np.ceil(self.master.get_final_status('fire') * 0.5)


name = '他山之石'
skill = [Skill_103001_1, Skill_103001_2, Skill_103001_3]
