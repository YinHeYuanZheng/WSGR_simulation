# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 狮(战巡)-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""提升全队战列、战巡 15 点火力值；
降低全队战列、战巡 5 点装甲值。"""


class Skill_104461_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(BB, BC))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0,
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            )
        ]


name = '突击'
skill = [Skill_104461_1]
