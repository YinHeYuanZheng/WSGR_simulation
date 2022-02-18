# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 埃罗芒什改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
"""支援航母(3级)：增加自身鱼雷机8点对潜值，增加自身轰炸机8点轰炸值。"""


class Skill_110231(Skill):
    def __init__(self, master):
        # todo 增加自身鱼雷机8点对潜值，增加自身轰炸机8点轰炸值。
        super().__init__(master)
        self.master = master
        self.target = SelfTarget(master)
        self.buff = [

        ]

    def is_active(self, friend, enemy):
        return True


skill = [Skill_110231]
