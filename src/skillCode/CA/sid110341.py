# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 摩耶-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""洋上的对空要塞(3级)：增加自身及相邻船只对空值9点，增加自己15%鱼雷值。"""


class Skill_110341_1(Skill):
    """增加自身及相邻船只对空值9点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(side=1,
                                       master=master,
                                       radius=1,
                                       direction='near',
                                       master_include=True)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]


class Skill_110341_2(CommonSkill):
    """增加自己15%鱼雷值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=2
            )
        ]


nae = '洋上的对空要塞'
skill = [Skill_110341_1, Skill_110341_2]
