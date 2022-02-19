# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 黄蜂改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
# todo 炮击战中，自身在受到伤害后对敌人发动反击，必然命中，伤害为普通攻击的100%。每场战斗限1次，(大破无法发动）


class Skill_112251(Skill):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = []

    def is_active(self, friend, enemy):
        return True


skill = [Skill_112251]
