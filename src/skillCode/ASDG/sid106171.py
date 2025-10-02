# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 南京-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队C国舰船航速增加3节，回避率和暴击率提高10%。
自身伤害提高30%，
当队伍中除了自身以外还有051型舰船时，全队暴击伤害和护甲穿透提高20%。"""


class Skill_106171_1(PrepSkill):
    """全队C国舰船航速增加3节"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='C')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='speed',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            )
        ]


class Skill_106171_2(Skill):
    """全队C国舰船回避率和暴击率提高10%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='C')
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='miss_rate',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
        ]


class Skill_106171_3(Skill):
    """自身伤害提高30%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.3,
            )
        ]


class Skill_106171_4(Skill):
    """当队伍中除了自身以外还有051型舰船时，全队暴击伤害和护甲穿透提高20%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='pierce_coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        type051 = TagTarget(side=1, tag='type051').get_target(friend, enemy)
        if self.master in type051:
            type051.remove(self.master)
        return len(type051)


name = '荣耀巡礼'
skill = [Skill_106171_1, Skill_106171_2, Skill_106171_3, Skill_106171_4]
