# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 天狼星改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""多面手巡洋舰(3级)：增加12点自身火力，增加20点对空值，
攻击中型和小型船有35%概率造成1.5倍伤害"""


class Skill_110501_1(CommonSkill):
    """增加12点自身火力，增加20点对空值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]


class Skill_110501_2(Skill):
    """攻击中型和小型船有35%概率造成1.5倍伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.5,
                atk_request=[BuffRequest_1],
                rate=0.35
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (MidShip, SmallShip))


name = '多面手巡洋舰'
skill = [Skill_110501_1, Skill_110501_2]
