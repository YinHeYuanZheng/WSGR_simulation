# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 让巴尔-舰队象征

"""舰队象征(3级)：增加自身携带的导弹装备12点火力值，全队舰船导弹战和闭幕导弹阶段受到的伤害降低50%。"""

from src.wsgr.equipment import Missile
from src.wsgr.phase import *
from src.wsgr.skill import *


class Skill_112992_1(Skill):
    """增加自身携带的导弹装备12点火力值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=(Missile,))
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]


class Skill_112992_2(Skill):
    """全队舰船导弹战和闭幕导弹阶段受到的伤害降低50%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            CoeffBuff(timer)
        ]


class CoeffBuff_1(CoeffBuff):
    def __init__(self, timer, phase=(MissilePhase), name='reduce_damage',
                 value=0, bias_or_weight=0, rate=1):
        super().__init__(timer, name, phase, value, bias_or_weight, rate)

    def is_active(self, damage, *args, **kwargs):
        self.value = np.floor(damage * 0.5)
        return True


skill = [Skill_112992_1, Skill_112992_2]
