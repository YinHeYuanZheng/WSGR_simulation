# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 信浓改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_112232_1(Skill):
    def __init__(self, timer, master):
        """航空战阶段，提升自身前方三个位置的航母、装母、轻母20%的伤害。"""
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=3,
            direction='up',
            shiptype=(CV, AV, CVL)
        )
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=(AirPhase,),
                value=0.2
            )
        ]


class Skill_112232_2(Skill):
    def __init__(self, timer, master):
        """当队伍中除了自己，不含有其他航母、轻母、装母时，
        增加自身装甲值35点，炮击战阶段，自身被攻击概率增加35%"""
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=(AllPhase,),
                value=35,
                bias_or_weight=0
            ),
            MagnetBuff(
                timer=timer,
                phase=(ShellingPhase,),
                rate=0.35
            )
        ]

    def is_active(self, friend, enemy):
        craft = TypeTarget(
            side=1,
            shiptype=(CV, CVL, AV)
        ).get_target(friend, enemy)
        craft.remove(self.master)
        return len(craft) == 0


class Skill_112232_3(PrepSkill):
    def __init__(self, timer, master):
        """当队伍中除了自己，不含有其他航母、轻母、装母时，增加自身索敌值25点"""
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=(AllPhase,),
                value=25,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        craft = TypeTarget(
            side=1,
            shiptype=(CV, CVL, AV)
        ).get_target(friend, enemy)
        craft.remove(self.master)
        return len(craft) == 0


skill = [Skill_112232_1, Skill_112232_2, Skill_112232_3]
