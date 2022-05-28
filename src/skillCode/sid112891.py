# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# U81

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身命中 +10，鱼雷 +10，被命中的敌人回避 -10 到昼战结束，对航母类(轻母，装母，航母)造成最终伤害增加 20%。"""


class Skill_112891_1(Skill):
    """自身命中 +10，鱼雷 +10，"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master, side=1)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=10,
                bias_or_weight=0,
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0,
            ),
        ]
class Skill_112891_2(Skill):
    """被命中的敌人回避 -10 到昼战结束"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master, side=1)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=DaytimePhase,
                buff=[StatusBuff(
                    timer=timer,
                    name='evastion',
                    phase=DaytimePhase,
                    value=-10,
                    bias_or_weight=0
                )],
                side=0
            )
        ]
class Skill_112891_3(Skill):
    """对航母类(轻母，装母，航母)造成最终伤害增加 20%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master, side=1)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=.2,
                atk_request=ATK_request_1,
            )
        ]
skill = [Skill_112891_1, Skill_112891_2, Skill_112891_3]
class ATK_request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (CV, CVL, AV))

