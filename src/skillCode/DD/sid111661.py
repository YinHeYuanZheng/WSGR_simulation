# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 阳炎改

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身有50%的概率参与开幕雷击。
闭幕鱼雷阶段有50%的概率额外发射一枚鱼雷。"""


class Skill_111661_1(Skill):
    """自身有50%的概率参与开幕雷击。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=FirstTorpedoPhase,
                rate=.5
            )
        ]


class Skill_111661_2(Skill):
    """闭幕鱼雷阶段有50%的概率额外发射一枚鱼雷。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='multi_torpedo_attack',
                phase=SecondTorpedoPhase,
                rate=.5
            )
        ]


name = '甲型驱逐舰'
skill = [Skill_111661_1, Skill_111661_2]
