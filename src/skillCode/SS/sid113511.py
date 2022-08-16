# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# U-1405

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""提升自身16闪避值，先制鱼雷阶段造成 15% 额外伤害。炮击战阶段降低对位的敌人9点命中值。"""


class Skill_113511_1(CommonSkill):
    """提升自身 16 闪避值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=16,
                bias_or_weight=0,
            )
        ]


class Skill_113511_2(Skill):
    """先制鱼雷阶段造成 15% 额外伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=FirstTorpedoPhase,
                value=.15,
            )
        ]


class Skill_113511_3(Skill):
    """炮击战阶段降低对位的敌人 9 点命中值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=0, loc=[self.master.loc])
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=ShellingPhase,
                value=-9,
                bias_or_weight=0,
            )
        ]


name = '潜行突袭'
skill = [Skill_113511_1, Skill_113511_2, Skill_113511_3]
