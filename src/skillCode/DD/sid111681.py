# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 黑潮改

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身有75%概率参与开幕雷击。
炮击战自身未造成伤害时，闭幕鱼雷阶段额外发射一枚鱼雷。"""


class Skill_111681_1(Skill):
    """自身有75%概率参与开幕雷击。"""
    def __init__(self, timer, master):
        self.target = SelfTarget(master)
        self.buff = [
            ActPhaseBuff(
                timer,
                name='act_phase',
                phase=FirstTorpedoPhase,
                rate=.75
            )
        ]

class Skill_111681_2(Skill):
    """炮击战自身未造成伤害时，闭幕鱼雷阶段额外发射一枚鱼雷。"""
    def __init__(self, timer, master):
        """Todo:没有对应标记"""
        self.target = SelfTarget(master)
    
    

name = '雷击特快'
skill = [Skill_111681_1, Skill_111681_2]
