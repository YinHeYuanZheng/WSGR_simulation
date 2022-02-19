# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 翔鹤改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from random import random


class Skill_112201(Skill):
    def __init__(self, master):
        """炮击战阶段时，25%概率代替队伍中其他航母、装母、轻母承受攻击，
        并获得80%伤害减免（每场战斗仅触发一次，且该技能大破状态不能发动）。"""
        super().__init__(master)
        self.flag = True
        self.master = master
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                name='',  # todo 伤害减免
                phase=(AllPhase,),  # todo 炮击战阶段
                value=0.8,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        if bool(self.request[0](self.master, friend, enemy)):
            if self.flag:
                self.flag = False
                return True
        return False


class Request_1(Request):
    def __bool__(self):
        # todo 检测炮击阶段航母受到攻击
        if random() <= 0.25 and self.master.damaged < 3:
            return True
        else:
            return False


skill = [Skill_112201]
