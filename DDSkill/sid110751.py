# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# Z16

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""己方所有Z系列驱逐命中提升 10 """


class Skill_110751_1(Skill):
    """己方所有Z系列驱逐命中提升 10 """
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='z-ship')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            
        ]
skill = [Skill_110751_1]