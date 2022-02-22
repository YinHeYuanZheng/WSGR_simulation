# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 光辉-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

class Skill_103701(Skill):
    """先驱首战(3级)：提升相邻上下航母，装母，轻母15点命中值和20%炮击战威力。"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = NearestLocTarget(side=1,
                                       master=master,
                                       radius=1,
                                       direction='near',
                                       shiptype=(CV, CVL, AV))
        self.buff = [StatusBuff(
            name='accuracy',
            phase=(AllPhase, ),
            value=15,
            bias_or_weight=0
        ), CoeffBuff(
            name='',  # todo 为炮击战时技能系数
            phase=(ShellingPhase,),
            value=0.2,
            bias_or_weight=2
        )]

    def is_active(self, friend, enemy):
        return True


class Request_1(Request):
    def __bool__(self):
        pass


skill = [Skill_103701]
