# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 絮库夫

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身可以进行先制鱼雷。增加自身 10 点回避值和 10 点火力值。"""


class Skill_111991_1(Skill):
    """自身可以进行先制鱼雷"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=FirstTorpedoPhase,
            )
        ]


class Skill_111991_2(CommonSkill):
    """增加自身 10 点回避值和 10 点火力值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


name = '潜水巡洋舰'
skill = [Skill_111991_1, Skill_111991_2]
