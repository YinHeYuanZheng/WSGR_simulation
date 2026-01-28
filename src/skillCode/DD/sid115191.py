# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# T.995改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队C国舰船索敌值增加6点，鱼雷值增加25点，先制鱼雷和鱼雷战阶段伤害提高25%。
队伍中每有1艘C国舰船，都会提高自身6%的回避率。"""


class Skill_115191_1(PrepSkill):
    """全队C国舰船索敌值增加6点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='C')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            )
        ]


class Skill_115191_2(Skill):
    """全队C国舰船鱼雷值增加25点，先制鱼雷和鱼雷战阶段伤害提高25%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='C')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=TorpedoPhase,
                value=0.25,
            )
        ]


class Skill_115191_3(Skill):
    """队伍中每有1艘C国舰船，都会提高自身6%的回避率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='miss_rate',
                phase=AllPhase,
                value=0.06,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        c_ship = CountryTarget(side=1, country='C').get_target(friend, enemy)
        c_num = len(c_ship)
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= c_num
                tmp_target.add_buff(tmp_buff)


name = '神机妙算'
skill = [Skill_115191_1, Skill_115191_2, Skill_115191_3]
