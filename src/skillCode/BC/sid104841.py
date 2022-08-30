# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 安森-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""队伍中每有一艘战巡都会增加自身 5% 暴击率和暴击伤害。"""


class Skill_104841(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.05,
                bias_or_weight=0,
            ),
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.05,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        num = len(TypeTarget(side=1, shiptype=BC).get_target(friend, enemy))
        for this_buff in self.buff[:]:
            buff = copy.copy(this_buff)
            buff.value *= num
            self.master.add_buff(buff)


name = '快速战队'
skill = [Skill_104841]
