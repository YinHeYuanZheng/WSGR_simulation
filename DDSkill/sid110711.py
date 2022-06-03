# -*- coding:utf-8 -*-
# Author:
# env:py38
# 电

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""
炮击战时15/25/35%概率发动，无视目标装甲对目标造成目标当前耐久值50%伤害(上限200点)，该次攻击必定命中(该技能大破状态不能发动)。
(伤害向上取整，最低造成1点伤害，即<400奇数血满血船直接中破。)"""


class Skill_110711_1(Skill):
    """炮击战时15/25/35%概率发动，无视目标装甲对目标造成目标当前耐久值50%伤害(上限200点)，该次攻击必定命中(该技能大破状态不能发动)。
(伤害向上取整，最低造成1点伤害，即<400奇数血满血船直接中破。)"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            
        ]
skill = [Skill_110711_1]