# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 黑潮改

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身有75%概率参与开幕雷击。
炮击战自身未造成伤害时，闭幕鱼雷阶段额外发射一枚鱼雷。"""


class Skill_111681_1(Skill):
    """自身有75%概率参与开幕雷击。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            ActPhaseBuff(
                timer,
                name='act_phase',
                phase=FirstTorpedoPhase,
                rate=.75
            )
        ]


class Skill_111681_2(Skill):
    """炮击战自身未造成伤害时，闭幕鱼雷阶段额外发射一枚鱼雷。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            DamageBasedBuff(
                timer=timer,
                name='multi_torpedo_attack',
                phase=SecondTorpedoPhase
            )
        ]


class DamageBasedBuff(SpecialBuff):
    def is_active(self, *args, **kwargs):
        damage = self.master.created_damage.get('FirstShellingPhase', 0) + \
                 self.master.created_damage.get('SecondShellingPhase', 0)
        return isinstance(self.timer.phase, self.phase) and \
               damage == 0


name = '雷击特快'
skill = [Skill_111681_1, Skill_111681_2]
