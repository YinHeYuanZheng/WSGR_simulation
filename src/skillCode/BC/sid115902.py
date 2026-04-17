# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 金伯恩-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""巡洋阵列(3级)：队伍中每有1艘战巡，增加全队舰船5点装甲值和回避值。
队伍中每有1艘S国主力舰，增加全队舰船5点火力值和命中值。
当全队战巡超过2艘时，每多超出一艘战巡，全队战巡依次增加获得如下效果：
伤害提高10%、暴击率提高10%、暴击伤害提高10%、装甲值增加15点。
"""


class Skill_115902_1(Skill):
    """队伍中每有1艘战巡，增加全队舰船5点装甲值和回避值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        count = len(TypeTarget(side=1, shiptype=BC).get_target(friend, enemy))
        if count == 0:
            return
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= count
                tmp_target.add_buff(tmp_buff)


class Skill_115902_2(Skill):
    """队伍中每有1艘S国主力舰，增加全队舰船5点火力值和命中值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        s_main = CombinedTarget(side=1,
                                target_list=[
                                    CountryTarget(side=1, country='S'),
                                    TypeTarget(side=1, shiptype=MainShip)
                                ]).get_target(friend, enemy)
        count = len(s_main)
        if count == 0:
            return
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= count
                tmp_target.add_buff(tmp_buff)


class Skill_115902_3(Skill):
    """当全队战巡超过2艘时，每多超出一艘战巡，全队战巡依次获得：
    伤害提高10%、暴击率提高10%、暴击伤害提高10%、装甲值增加15点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=BC)
        self.buff = []
        self.extra_buffs = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.1
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        if len(target) <= 2:
            return
        skill_num = len(target) - 2
        for tmp_target in target:
            for tmp_buff in self.extra_buffs[:skill_num]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_target.add_buff(tmp_buff)


name = '巡洋阵列'
skill = [Skill_115902_1, Skill_115902_2, Skill_115902_3]
