# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 波特

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""战斗中，全队驱逐舰命中+6，鱼雷值+6，敌方驱逐舰命中-12。"""


class Skill_111821_1(Skill):
    """战斗中，全队驱逐舰命中+6，鱼雷值+6，"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=DD)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
        ]
    
class Skill_111821_2(Skill):
    """敌方驱逐舰命中-12"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=DD)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-12,
                bias_or_weight=0
            ),

        ]
        
name = '统率力'
skill = [Skill_111821_1, Skill_111821_2]
