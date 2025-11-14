# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 前卫-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身15点火力值、命中值和索敌值。
自身受到40点以上伤害时，伤害将降低到40点。
炮击战阶段自身受到伤害后对攻击的敌人发动反击，该次反击的攻击威力不会因耐久损伤而降低且必定命中
（每场战斗触发一次，大破无法发动）。"""


class Skill_111052_1(CommonSkill):
    """增加自身15点火力值、命中值和索敌值。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_111052_2(Skill):
    """自身受到40点以上伤害时，伤害将降低到40点。
    炮击战阶段自身受到伤害后对攻击的敌人发动反击，该次反击的攻击威力不会因耐久损伤而降低且必定命中
    （每场战斗触发一次，大破无法发动）。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CapShield(
                timer=timer,
                phase=AllPhase,
                cap_value=40
            ),
            HitBack(
                timer=timer,
                phase=ShellingPhase,
                coef={'ignore_damaged': True}
            )
        ]


class CapShield(CoeffBuff):
    def __init__(self, timer, phase, cap_value,
                 name='reduce_damage', value=0, bias_or_weight=0, rate=1):
        super().__init__(timer, name, phase, value, bias_or_weight, rate)
        self.cap_value = cap_value

    def change_value(self, damage, *args, **kwargs):
        self.value = max(0, damage - self.cap_value)


name = '火力平台'
skill = [Skill_111052_1, Skill_111052_2]
