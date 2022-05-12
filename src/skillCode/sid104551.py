# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 皇家方舟(av)-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""新时代(3级)：提升自身12点火力值。
炮击战阶段，自身可以参与次轮炮击战，火力为首轮炮击120%。"""


class Skill_104551_1(CommonSkill):
    """提升自身12点火力值。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=(AllPhase,),
                value=12,
                bias_or_weight=0
            )
        ]


class Skill_104551_2(Skill):
    """炮击战阶段，自身可以参与次轮炮击战，火力为首轮炮击120%。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=SecondShellingPhase
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=SecondShellingPhase,
                value=0.2,
                bias_or_weight=1)
        ]


skill = [Skill_104551_1, Skill_104551_2]
