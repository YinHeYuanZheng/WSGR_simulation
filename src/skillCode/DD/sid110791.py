# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# Z28改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队G国护卫舰火力值、鱼雷值、回避值、对空值、索敌值和命中值增加6点。
全队Z系列驱逐攻击威力提高15%，回避率提高9%，当自身为旗舰时，提高的数值为双倍。"""


class Skill_110791_1(Skill):
    """全队G国护卫舰火力值、鱼雷值、回避值、对空值和命中值增加6点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[CountryTarget(side=1, country='G'),
                         TypeTarget(side=1, shiptype=CoverShip)]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
        ]


class Skill_110791_2(PrepSkill):
    """全队G国护卫舰索敌值增加6点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[CountryTarget(side=1, country='G'),
                         TypeTarget(side=1, shiptype=CoverShip)]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
        ]


class Skill_110791_3(Skill):
    """全队Z系列驱逐攻击威力提高15%，回避率提高9%，当自身为旗舰时，提高的数值为双倍。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='z-ship')
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='power_buff',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=2
            ),
            CoeffBuff(
                timer=timer,
                name='miss_rate',
                phase=AllPhase,
                value=0.09,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                if self.master.loc == 1:
                    tmp_buff.value *= 2
                tmp_target.add_buff(tmp_buff)


name = 'Z驱旗舰'
skill = [Skill_110791_1, Skill_110791_2, Skill_110791_3]
