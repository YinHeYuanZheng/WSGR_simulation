# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 皇家方舟(av)-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *


class Skill_104551_1(CommonSkill):
    """新时代(3级)：提升自身12点火力值。
    炮击战阶段，自身可以参与次轮炮击战，火力为首轮炮击120%。
"""
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [CommonBuff(
            name='fire',
            phase=(AllPhase, ),
            value=12,
            bias_or_weight=0
        )]


class Skill_104551_2(Skill):
    """炮击战阶段，自身可以参与次轮炮击战，火力为首轮炮击120%。"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [StatusBuff(
            name='fire',
            phase=(SecondShellingPhase, ),
            value=0.2 * master.status['fire'],
            bias_or_weight=0
        ), StatusBuff(
            name='range',
            phase=(AllPhase,),
            value=3,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        return True


class Request_1(Request):
    def __bool__(self):
        pass


skill = [Skill_104551_1]
