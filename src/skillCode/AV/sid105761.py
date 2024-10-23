# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 中途岛

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队航母舰载机威力提升10%，全队装母、轻母舰载机威力提升15%。
战斗中自身根据敌方主力舰数量，依次获得如下效果：
命中率提高20%、暴击伤害增加20%、暴击率提高20%、
舰载机威力提高20%、攻击威力不会因耐久损伤而降低、攻击时降低敌方100%对空值（不包含装备）"""


class Skill_105761_1(Skill):
    """全队航母舰载机威力提升10%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=CV)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=2
            )
        ]


class Skill_105761_2(Skill):
    """全队装母、轻母舰载机威力提升15%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(AV, CVL))
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=2
            )
        ]


class Skill_105761_3(Skill):
    """战斗中自身根据敌方主力舰数量，依次获得如下效果：
    命中率提高20%、暴击伤害增加20%、暴击率提高20%、
    舰载机威力提高20%、攻击威力不会因耐久损伤而降低、攻击时降低敌方100%对空值（不包含装备）"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=2
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase,
            ),
            AtkBuff(
                timer=timer,
                name='ignore_antiair',
                phase=AllPhase,
                value=-1,
                bias_or_weight=1,
            )
        ]

    def activate(self, friend, enemy):
        # 获取敌方主力舰数量
        count = len(TypeTarget(side=0, shiptype=MainShip
                               ).get_target(friend, enemy))
        # 根据敌方主力舰数量，依次获得效果
        for i in range(count):
            tmp_buff = copy.copy(self.buff[i])
            self.master.add_buff(tmp_buff)


name = '舰队精锐'
skill = [Skill_105761_1, Skill_105761_2, Skill_105761_3]
