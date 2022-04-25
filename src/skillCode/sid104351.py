# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# B65

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""huan_yp:
write on 2022.4.24
recheck on 2022.4.25
"""

"""当自身为旗舰时，炮击战阶段提升全队中、小型船 10 点回避值
，夜战阶段提升中型船 13 点火力值
和小型船 10 点鱼雷值"""

class Skill_104351_1(Skill):
    """当自身为旗舰时，炮击战阶段提升全队中、小型船 10 点回避值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target=TypeTarget(1,(SmallShip,MidShip))
        self.buff=[
            StatusBuff(timer=timer,
                name="evasion",
                phase=ShellingPhase,
                value=10,
                bias_or_weight=0,
            )
        ]
    def activate(self, friend, enemy):
        if(self.master.loc != 1): return
        return super().activate(friend, enemy)

class Skill_104351_2(Skill):
    """(当自身为旗舰时)夜战阶段提升中型船5/9/13点火力值
        """
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target=TypeTarget(1,(MidShip))
        self.buff=[
            StatusBuff(timer=timer,
                name="fire",
                phase=NightPhase,
                value=13,
                bias_or_weight=0
            )
        ]
    def activate(self, friend, enemy):
        if(self.master.loc != 1):return 
        return super().activate(friend, enemy)
class Skill_104351_3(Skill):
    """
        (当自身为旗舰时)(夜战阶段)小型船 10 点鱼雷值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target=TypeTarget(1,(SmallShip))
        self.buff=[
            StatusBuff(timer=timer,
                name="torpedo",
                phase=NightPhase,
                value=10,
                bias_or_weight=0
            )
        ]
    def activate(self, friend, enemy):
        if(self.master.loc != 1):return 
        return super().activate(friend, enemy)
skill = [Skill_104351_1,Skill_104351_2,Skill_104351_3]