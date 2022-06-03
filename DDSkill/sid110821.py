# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 萤火虫-无畏撞击

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""
炮击战时40%概率发动，无视目标装甲对目标造成自身装甲40/60/80%的固定伤害，该次攻击必定命中。"""
class Skill_110821_1(Skill):
    """炮击战时40%概率发动，无视目标装甲对目标造成自身装甲40/60/80%的固定伤害，该次攻击必定命中。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            
        ]
            
skill = [Skill_110821_1]