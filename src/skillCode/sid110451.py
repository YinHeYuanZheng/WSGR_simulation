# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 五十铃改

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""装备的防空炮将同时视为对潜装备。并且防空炮的对空值的 80% 视为对潜值。
装备的对潜装备同时视为防空炮，并且对潜装备的对潜值的 80% 视为对空值。"""


class Skill_110451(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [

        ]
    def activate(self, friend, enemy):
        """ToDo:等接口

        """
        




name = '空潜一体'
skill = [Skill_110451]
