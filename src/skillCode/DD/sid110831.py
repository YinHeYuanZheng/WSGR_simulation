# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 标枪

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""最大耐久增加11，每次战斗中能免疫一次致命伤害。"""


class Skill_110831_1(CommonSkill):
    """最大耐久增加11"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='health',
                phase=AllPhase,
                value=11,
                bias_or_weight=0,
            )
        ]


class Skill_110831_2(Skill):
    """每次战斗中能免疫一次致命伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            RecoverShield(timer=timer)
        ]


class RecoverShield(CoeffBuff):
    def __init__(self, timer, phase=AllPhase, name='reduce_damage',
                 value=0, bias_or_weight=0, rate=1):
        super().__init__(timer, name, phase, value, bias_or_weight, rate)
        self.exhaust = 1

    def is_active(self, damage, *args, **kwargs):
        if self.exhaust == 0:
            return False

        master_health = self.master.status['health']
        if damage > master_health:
            self.value = damage - master_health + 1
            self.exhaust -= 1
            return True
        else:
            return False


name = '绝境逢生'
skill = [Skill_110831_1, Skill_110831_2]
