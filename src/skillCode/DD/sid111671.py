# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 不知火

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身所携带鱼雷装备5点鱼雷值；
队伍中有雷击值的角色大于等于3时，增加自身闭幕雷击阶段12点命中值和15%暴击率。"""

class Skill_111671_1(Skill):
    """增加自身所携带鱼雷装备5点鱼雷值。"""
    def __init__(self, timer, master):
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=(Torpedo,))
        
        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=(AllPhase,),
                value=5,
                bias_or_weight=0
            )
        ]

class Skill_111671_2(Skill):
    """队伍中有雷击值的角色大于等于3时，增加自身闭幕雷击阶段12点命中值和15%暴击率。"""
    def __init__(self, timer, master):
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=SecondTorpedoPhase,
                value=12,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=SecondTorpedoPhase,
                value=.15,
                bias_or_weight=0,
            )
        ]
    def is_active(self, friend, enemy):
        count = 0 
        for ship in friend:
            if ship.get_final_status('torpedo') > 0:
                count += 1
        return count >= 3

name = '雷击战突进'
skill = [Skill_111671_1, Skill_111671_2]
