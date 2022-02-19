# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 扶桑改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110021_1(Skill):
    # todo 提升自身所装备的大口径主炮类装备的火力5点，单纵或者梯形阵时增加自身火力5点和命中15点。
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = []

    def is_active(self, friend, enemy):
        return True


class Skill_110021_2(Skill):
    # 单纵或者梯形阵时增加自身火力5点和命中15点。
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.request = [Request_1]
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
        return bool(self.request[0](self.master, friend, enemy))


class Request_1(Request):
    def __bool__(self):
        # todo 检索阵型
        pass


skill = [Skill_110021_2]
