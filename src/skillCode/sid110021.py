# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 扶桑改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *


class Skill_110021_1(CommonSkill):
    # 提升自身所装备的大口径主炮类装备的火力5点。
    def __init__(self, master):
        super().__init__(master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=(MainGun, ))
        self.buff = [CommonBuff(
            name='fire',
            phase=(AllPhase,),
            value=5,
            bias_or_weight=0
        )]


class Skill_110021_2(Skill):
    # 单纵或者梯形阵时增加自身火力5点和命中15点。
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                name='fire',
                phase=(AllPhase,),
                value=5,
                bias_or_weight=0
            ), StatusBuff(
                name='accuracy',
                phase=(AllPhase,),
                value=15,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return friend.form == 1 or friend.form == 4


skill = [Skill_110021_1, Skill_110021_2]
