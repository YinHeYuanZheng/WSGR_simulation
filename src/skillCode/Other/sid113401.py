# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 波尔扎诺-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身装备的战斗机对空值提高60%。
当队伍中护卫舰数量≥2时，自身因战斗造成的舰载机损失减少50%。
降低敌方护卫舰12点命中值和装甲值。全队I国舰船暴击率提升10%。"""


class Skill_113401_1(CommonSkill):
    """自身装备的战斗机对空值提高60%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(
            side=1,
            target=SelfTarget(master),
            equiptype=Fighter
        )
        self.buff = [
            CommonBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=0.6,
                bias_or_weight=1
            )
        ]


class Skill_113401_2(Skill):
    """当队伍中护卫舰数量≥2时，自身因战斗造成的舰载机损失减少50%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='fall_rest',
                phase=AirPhase,
                value=-0.5,
                bias_or_weight=1,
            )
        ]

    def is_active(self, friend, enemy):
        cover = TypeTarget(side=0, shiptype=CoverShip
                           ).get_target(friend, enemy)
        return len(cover) >= 2


class Skill_113401_3(Skill):
    """降低敌方护卫舰12点命中值和装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=CoverShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-12,
                bias_or_weight=0
            )
        ]


class Skill_113401_4(Skill):
    """全队I国舰船暴击率提升10%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='I')
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]


name = '特别空袭'
skill = [Skill_113401_1, Skill_113401_2, Skill_113401_3, Skill_113401_4]
