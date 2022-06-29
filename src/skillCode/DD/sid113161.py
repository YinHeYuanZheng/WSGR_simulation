# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 明斯克改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.formulas import AirAtk

"""漫长战役(3级)：免疫自身受到的第一次航空攻击（限昼战）；
根据战斗点距离出发点的位置降低敌方战斗力，离初始点越远降低越多（最高5层），
每阶段降低敌方全体3点命中值、5点闪避值、4点装甲值。
"""


class Skill_113161_1(Skill):
    """免疫自身受到的第一次航空攻击（限昼战）"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='shield',
                phase=DaytimePhase,
                exhaust=1,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, AirAtk)


class Skill_113161_2(Skill):
    """根据战斗点距离出发点的位置降低敌方战斗力，离初始点越远降低越多（最高5层），
    每阶段降低敌方全体3点命中值、5点闪避值、4点装甲值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=0)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-4,
                bias_or_weight=0
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


skill = [Skill_113161_1, Skill_113161_2]
