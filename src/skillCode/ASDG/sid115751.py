# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 威武改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from AADG_common import *

"""全队S国舰船对空值增加30点，航空战阶段回避率提高20%，战斗结算获得的经验提高25%。
队伍中每有1艘S国舰船都会提高自身10%伤害。
自身装备的发射器会视为反潜装备，其索敌值视为对潜值。"""


class Skill_115751_1(Skill):
    """全队S国舰船对空值增加30点，航空战阶段回避率提高20%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='S')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='miss_rate',
                phase=AirPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]


class Skill_115751_2(Skill):
    """队伍中每有1艘S国舰船都会提高自身10%伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.1
            )
        ]

    def activate(self, friend, enemy):
        S_num = len(CountryTarget(side=1, country='S'
                                  ).get_target(friend, enemy))
        buff0 = copy.copy(self.buff[0])
        buff0.value *= S_num
        self.master.add_buff(buff0)


name = '特化先驱'
skill = [Skill_115751_1, Skill_115751_2, AADGCommonSkill]
