# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# Z18

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""威瑟堡行动(3级)：Z18增加自己索敌20点，增加对应位置敌舰火力10点、暴击率5%、被攻击概率降低30%（水下单位或自身旗舰时无效）。
"""


class Skill_112701_1(CommonSkill):
    """Z18增加自己索敌20点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CommonBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


class Skill_112701_2(Skill):
    """增加对应位置敌舰火力10点、暴击率5%、被攻击概率降低30%（水下单位或自身旗舰时无效）。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SkillTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.05,
                bias_or_weight=0
            ),
            UnMagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.3
            )
        ]


class SkillTarget(SelfTarget):
    def get_target(self, friend, enemy):
        lead = LocTarget(side=0, loc=[1])\
            .get_target(friend=friend, enemy=enemy)
        opposite = LocTarget(side=0, loc=[self.master.loc])\
            .get_target(friend=friend, enemy=enemy)

        target = []
        if opposite != lead and not isinstance(opposite, Submarine):
            target.append(opposite)

        return target


name = '威瑟堡行动'
skill = [Skill_112701_1, Skill_112701_2]
