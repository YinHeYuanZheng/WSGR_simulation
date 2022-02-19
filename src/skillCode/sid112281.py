# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 隼鹰改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_112281(Skill):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.request = [Request_1]
        self.buff = [
            CoeffBuff(
                name='',  # todo 终伤倍率
                phase=(AllPhase,),
                value=0.25,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        return bool(self.request[0](self.master, friend, enemy))


class Request_1(Request):
    def __bool__(self):
        # todo 查找攻击目标
        pass

skill = [Skill_112281]
