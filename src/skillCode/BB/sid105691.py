# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 布勃诺夫方案

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身可免疫1次伤害。
当敌方主力舰≤3时，自身装甲值和命中值增加20点。
当敌方主力舰≥5时，自身装甲值降低30%，自身和舰队旗舰的火力值增加自身的装甲值。"""


class Skill_105691_1(Skill):
    """自身可免疫1次伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            DamageShield(
                timer=timer,
                phase=AllPhase,
            )
        ]


class Skill_105691_2(Skill):
    """当敌方主力舰≤3时，自身装甲值和命中值增加20点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
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
                name='accuracy',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        # 获取敌方主力舰数量
        count = len(TypeTarget(side=0, shiptype=MainShip
                               ).get_target(friend, enemy))
        return count <= 3


class Skill_105691_3(Skill):
    """当敌方主力舰≥5时，自身装甲值降低30%，自身和舰队旗舰的火力值增加自身的装甲值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-0.3,
                bias_or_weight=1
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=0,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        # 获取敌方主力舰数量
        count = len(TypeTarget(side=0, shiptype=MainShip
                               ).get_target(friend, enemy))
        return count >= 5

    def activate(self, friend, enemy):
        buff_1 = copy.copy(self.buff[0])
        self.master.add_buff(buff_1)

        if self.master.loc == 1:
            target = [self.master]
        else:
            target = [self.master, friend.ship[0]]

        armor = self.master.get_final_status('armor')  # 获取自身的装甲值
        for tmp_target in target:
            buff_2 = copy.copy(self.buff[1])
            buff_2.value = armor
            tmp_target.add_buff(buff_2)


name = '海啸'
skill = [Skill_105691_1, Skill_105691_2, Skill_105691_3]
