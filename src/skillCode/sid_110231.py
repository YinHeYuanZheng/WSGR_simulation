# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 加贺改-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *


class Skill_110231(Skill):
    def __init__(self, master):
        super().__init__(master)
        self.target = SelfTarget(master)
        self.buff = []

    def is_active(self, friend, enemy):
        return True


skill = [Skill_110231]
