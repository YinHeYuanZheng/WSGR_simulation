# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 逸仙改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""矢志不渝(3级)：提升全队的装甲、回避、对空值5点，对C国船只3倍效果。"""


class Skill_111621(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                if tmp_target.status['country'] == 'C':
                    tmp_buff.value *= 3
                tmp_target.add_buff(tmp_buff)


skill = [Skill_111621]
