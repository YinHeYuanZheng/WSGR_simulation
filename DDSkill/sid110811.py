# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 紫石英

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""
自身被攻击概率提高 22%，自身回避 11。"""
class Skill_110811_1(Skill):
    """自身被攻击概率提高 22%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=.22
            ),
            
        ]
class Skill_110811_2(CommonSkill):
    """自身回避 +11。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=11,
                bias_or_weight=0
            ),
            
        ]
            
skill = [Skill_110811_1, Skill_110811_2]