# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 罗斯福-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""敌方舰船火力值、对空值、装甲值、回避值降低20点。
根据战斗点距离起始点的位置提升全队U国和E国舰船战斗力，离初始点越远战斗力越高，
每层提高4%舰载机威力(演习、战役、决战、立体强袭、模拟演习为满层5层)。"""


class Skill_106191_1(Skill):
    """敌方舰船火力值、对空值、装甲值、回避值降低20点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=0)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-20,
                bias_or_weight=0,
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=-20,
                bias_or_weight=0,
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-20,
                bias_or_weight=0,
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-20,
                bias_or_weight=0,
            ),
        ]


class Skill_106191_2(Skill):
    """根据战斗点距离起始点的位置提升全队U国和E国舰船战斗力，离初始点越远战斗力越高，
    每层提高4%舰载机威力(演习、战役、决战、立体强袭、模拟演习为满层5层)。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='UE')
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.04,
                bias_or_weight=2
            )
        ]

    def activate(self, friend, enemy):
        buff_mul = self.timer.get_dist()
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= buff_mul
                tmp_target.add_buff(tmp_buff)


name = '地中海女王'
skill = [Skill_106191_1, Skill_106191_2]
