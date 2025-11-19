# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 亚特兰大-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队舰船对空值增加30点，航空战阶段回避率提高15%。
当队伍中除了亚特兰大以外还有别的亚特兰大级舰船时，敌方随机1艘航母航空战阶段无法行动，
全队U国护卫舰装甲、回避、对空值增加20点"""


class Skill_110561_1(Skill):
    """全队舰船对空值增加30点，航空战阶段回避率提高15%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
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
                value=0.15,
                bias_or_weight=0
            )
        ]


class Skill_110561_2(Skill):
    """当队伍中除了亚特兰大以外还有别的亚特兰大级舰船时，敌方随机1艘航母航空战阶段无法行动"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = RandomTypeTarget(side=0, shiptype=CV)
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='not_act_phase',
                phase=AirPhase,
            )
        ]

    def is_active(self, friend, enemy):
        target_atlanta = TagTarget(side=1, tag='atlanta').get_target(friend, enemy)
        if self.master in target_atlanta:
            target_atlanta.remove(self.master)  # 去除自身
        return len(target_atlanta)


class Skill_110561_3(Skill):
    """当队伍中除了亚特兰大以外还有别的亚特兰大级舰船时，全队U国护卫舰装甲、回避、对空值增加20点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                CountryTarget(side=1, country='U'),
                TypeTarget(side=1, shiptype=CoverShip),
            ]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
        ]


name = '对空防御'
skill = [Skill_110561_1, Skill_110561_2, Skill_110561_3]
