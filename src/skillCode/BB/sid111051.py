# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 前卫-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""	根据战斗点距离起始点的位置提升自身战斗力，离初始点越远战斗力越高，
每层火力、装甲、对空、命中、回避增加3点，暴击率提升3%(演习、战役、决战、立体强袭、模拟演习为满层5层)"""


class Skill_111051(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.03,
                bias_or_weight=0
            ),
        ]

    def activate(self, friend, enemy):
        buff_mul = self.timer.get_dist()
        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            tmp_buff.value *= buff_mul
            self.master.add_buff(tmp_buff)


name = '皇家游轮'
skill = [Skill_111051]
