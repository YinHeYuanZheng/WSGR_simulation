# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 克劳塞维茨-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身炮击战阶段 40% 概率同时攻击2个目标,队伍中每有 1 艘 G 国船都会增加 10% 发动概率。
队伍中主力舰≥3时，提升全队 10 点火力值和命中值。
队伍中护卫舰≥3时，提升全队 10 点装甲值和回避值。"""


class Skill_104901_1(Skill):
    """自身炮击战阶段 40% 概率同时攻击2个目标,队伍中每有 1 艘 G 国船都会增加 10% 发动概率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.buff = [
            MultipleAtkBuff(
                timer=timer,
                name='multi_attack',
                phase=ShellingPhase,
                num=2,
                rate=0.4
            ),
        ]

    def activate(self, friend, enemy):
        num = len(CountryTarget(side=1, country="G").get_target(friend, enemy))
        buff = copy.copy(self.buff[0])
        buff.rate += num * 0.1
        buff.rate = min(1., buff.rate)
        self.master.add_buff(buff)


class Skill_104901_2(Skill):
    """队伍中主力舰≥3时，提升全队 10 点火力值和命中值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        main_ship = TypeTarget(side=1, shiptype=MainShip).get_target(friend, enemy)
        return len(main_ship) >= 3


class Skill_104901_3(Skill):
    """队伍中护卫舰≥3时，提升全队 10 点装甲值和回避值。。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        cover_ship = TypeTarget(side=1, shiptype=CoverShip).get_target(friend, enemy)
        return len(cover_ship) >= 3


skill = [Skill_104901_1, Skill_104901_2, Skill_104901_3]
