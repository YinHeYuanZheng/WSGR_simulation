# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 1913战巡-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身火力、装甲、对空、命中、回避、索敌、幸运属性增加图鉴中开启的C国船数量*1。
根据队伍中C国船的数量，全队舰船战斗中依次获得如下效果：
火力值增加8点、装甲值增加8点、回避值增加8点、暴击率增加8%、暴击伤害增加10%、全阶段免疫1次伤害。"""


class Skill_105211_1(CommonSkill):
    """自身火力、装甲、对空、命中、回避、索敌、幸运属性增加图鉴中开启的C国船数量*1。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        buff_value = 23
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='luck',
                phase=AllPhase,
                value=buff_value,
                bias_or_weight=0
            ),
        ]


class Skill_105211_2(Skill):
    """根据队伍中C国船的数量，全队舰船战斗中依次获得如下效果：
    火力值增加8点、装甲值增加8点、回避值增加8点、暴击率增加8%、暴击伤害增加10%、全阶段免疫1次伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.08,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            DamageShield(
                timer=timer,
                phase=AllPhase,
            )
        ]

    def activate(self, friend, enemy):
        # 获取C国数量
        count = len(CountryTarget(side=1, country='C'
                                  ).get_target(friend, enemy))
        target = self.target.get_target(friend, enemy)
        # 根据C国数量，依次获得效果
        for tmp_target in target:
            for i in range(count):
                tmp_buff = copy.copy(self.buff[i])
                tmp_target.add_buff(tmp_buff)


name = '巨舰梦想'
skill = [Skill_105211_1, Skill_105211_2]
