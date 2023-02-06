# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 深海111号战列

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""从鬼武士身上获得了神秘力量。
炮击战阶段敌方每一艘主力舰都会增加全体5点装甲值和5点回避值,
全阶段敌方每一艘护卫舰都会降低全体10点装甲值和10点回避值,
炮击战阶段自身会同时攻击3个目标。"""


class Skill_010471_1(Skill):
    """炮击战阶段敌方每一艘主力舰都会增加全体5点装甲值和5点回避值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=ShellingPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=ShellingPhase,
                value=5,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        buff_num = len(TypeTarget(side=0, shiptype=MainShip)
                       .get_target(friend, enemy))
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= buff_num
                tmp_target.add_buff(tmp_buff)


class Skill_010471_2(Skill):
    """全阶段敌方每一艘护卫舰都会降低全体10点装甲值和10点回避值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        buff_num = len(TypeTarget(side=0, shiptype=MainShip)
                       .get_target(friend, enemy))
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= buff_num
                tmp_target.add_buff(tmp_buff)


class Skill_010471_3(Skill):
    """炮击战阶段自身会同时攻击3个目标"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MultipleAtkBuff(
                timer=timer,
                name='multi_attack',
                phase=ShellingPhase,
                num=3,
                rate=1
            )
        ]


name = '毁灭打击'
skill = [Skill_010471_1, Skill_010471_2, Skill_010471_3]
