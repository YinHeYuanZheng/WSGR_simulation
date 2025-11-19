# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 费拉迪D-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""降低敌方舰船15点命中值；
费拉迪D会随机选择2艘敌方舰船降低其50%回避值并提高其50%所受到的伤害，
当队伍中I国舰船≥3时，再降低其50%装甲值。"""


class Skill_103211_1(Skill):
    """降低敌方舰船15点命中值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=0)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            )
        ]


class Skill_103211_2(Skill):
    """费拉迪D会随机选择2艘敌方舰船降低其50%回避值并提高其50%所受到的伤害，
    当队伍中I国舰船≥3时，再降低其50%装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = RandomTarget(side=0, num=2)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-0.5,
                bias_or_weight=1
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=0.5
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-0.5,
                bias_or_weight=1
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.cid in ['10321', '11321']

    def activate(self, friend, enemy):
        shipI = CountryTarget(side=1, country='I'
                              ).get_target(friend, enemy)
        if len(shipI) >= 3:
            buff_slice = 3
        else:
            buff_slice = 2

        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:buff_slice]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_target.add_buff(tmp_buff)


name = '海神谴戒'
skill = [Skill_103211_1, Skill_103211_2]
