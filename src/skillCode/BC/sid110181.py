# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 声望-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""最后的荣耀: 根据战斗点距离起始点的位置提升自身战斗力，离初始点越远战斗力越高，
每层火力、装甲、对空、命中、回避增加4点，暴击率提升4%(演习、战役、决战、立体强袭、模拟演习为5层满)。
全队E国战巡额外增加20%暴击伤害"""


class Skill_110181_1(Skill):
    """根据战斗点距离起始点的位置提升自身战斗力，离初始点越远战斗力越高，
    每层火力、装甲、对空、命中、回避增加4点，暴击率提升4%(演习、战役、决战、立体强袭、模拟演习为5层满)。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.04,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        buff_mul = self.timer.get_dist()
        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            tmp_buff.value *= buff_mul
            self.master.add_buff(tmp_buff)


class Skill_110181_2(Skill):
    """全队E国战巡额外增加20%暴击伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                CountryTarget(side=1, country='E'),
                TypeTarget(side=1, shiptype=BC),
            ]
        )
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]


name = '最后的荣耀'
skill = [Skill_110181_1, Skill_110181_2]
