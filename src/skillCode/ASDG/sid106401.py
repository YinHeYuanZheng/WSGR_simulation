# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 考文垂-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from AADG_common import *

"""防空区域(3级)：自身对空值的50%视为火力值，装备的发射器会视为反潜装备，其索敌值视为对潜值。
昼战阶段自身被攻击概率提高20%，自身和队伍中的航母、轻母免疫敌方对空值低于100的舰船造成的伤害。
全队小型船火力值增加自身30%的对空值。全队E国小型船火力值增加自身30%的对空值。
"""


class Skill_106401_1(CommonSkill):
    """自身对空值的50%视为火力值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=.5,
                bias_or_weight=0
            ),
        ]

    def activate(self, friend, enemy):
        antiair_value = self.master.get_final_status('antiair')
        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            tmp_buff.value *= antiair_value
            self.master.add_buff(tmp_buff)


class Skill_106401_2(Skill):
    """昼战阶段自身被攻击概率提高20%，自身免疫敌方对空值低于100的舰船造成的伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=DaytimePhase,
                rate=0.2
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=DaytimePhase,
                value=-1,
                atk_request=[ATKRequest_LowAntiair]
            )
        ]


class Skill_106401_3(Skill):
    """昼战阶段队伍中的航母、轻母免疫敌方对空值低于100的舰船造成的伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(CV, CVL))
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=DaytimePhase,
                value=-1,
                atk_request=[ATKRequest_LowAntiair]
            )
        ]


class Skill_106401_4(Skill):
    """全队小型船火力值增加自身30%的对空值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=SmallShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        antiair_value = self.master.get_final_status('antiair')
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= antiair_value
                tmp_target.add_buff(tmp_buff)


class Skill_106401_5(Skill):
    """全队E国小型船火力值增加自身30%的对空值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                CountryTarget(side=1, country='E'),
                TypeTarget(side=1, shiptype=SmallShip)
            ])
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        antiair_value = self.master.get_final_status('antiair')
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= antiair_value
                tmp_target.add_buff(tmp_buff)


class ATKRequest_LowAntiair(ATKRequest):
    """攻击方对空值低于100"""
    def __bool__(self):
        return self.atk.source.get_final_status('antiair') < 100


name = '防空区域'
skill = [Skill_106401_1, Skill_106401_2, Skill_106401_3,
         Skill_106401_4, Skill_106401_5, AADGCommonSkill]
