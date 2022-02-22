# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 汉考克-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *


class Skill_103741_1(Skill):
    """增加自身装备的轰炸机的轰炸值4点。"""

    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=(Bomber,))
        self.buff = [StatusBuff(
            name='bomb',
            phase=(AllPhase,),
            value=4,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        return True


class Skill_103741_2(Skill):
    """队伍中航母装母总数量小于3时，提升自身火力值10点；"""

    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [StatusBuff(
            name='fire',
            phase=(AllPhase,),
            value=10,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        return bool(self.request[0](master=self.master, friend=friend, enemy=enemy))


class Skill_103741_3(Skill):
    """队伍中航母装母总数量大于等于3时，提升自身装甲值9点与命中值9点。"""

    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [StatusBuff(
            name='armor',
            phase=(AllPhase,),
            value=9,
            bias_or_weight=0
        ), StatusBuff(
            name='accuracy',
            phase=(AllPhase,),
            value=9,
            bias_or_weight=0
        )]

    def is_active(self, friend, enemy):
        if bool(self.request[0](master=self.master, friend=friend, enemy=enemy)):
            return False
        return True


class Request_1(Request):
    def __bool__(self):
        return len(TypeTarget(side=1, shiptype=(CV, AV)).get_target(self.friend, self.enemy)) < 3


skill = [Skill_103741_1, Skill_103741_2, Skill_103741_3]
