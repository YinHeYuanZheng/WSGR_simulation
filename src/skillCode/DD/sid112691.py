# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# z-17改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身回避减少10点，被攻击概率提高30%。
敌方队伍在自身对应位置的水上舰船的回避减少40，火力减少40，被攻击概率提高30%。"""


class Skill_112691_1(CommonSkill):
    """自身回避减少10"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-10,
                bias_or_weight=0
            )
        ]


class Skill_112691_2(Skill):
    """敌方队伍在自身对应位置的水上舰船的回避减少40，火力减少40，被攻击概率提高30%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=0, loc=[master.loc])
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-40,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-40,
                bias_or_weight=0
            ),
            MagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.3
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            if isinstance(tmp_target, Submarine):
                continue
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_target.add_buff(tmp_buff)


class Skill_112691_3(Skill):
    """自身被攻击概率提高30%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.3
            )
        ]


name = '纳尔维克警戒'
skill = [Skill_112691_1, Skill_112691_2, Skill_112691_3]
