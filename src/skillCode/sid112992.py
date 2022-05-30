# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 让巴尔-舰队象征

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.equipment import Missile

"""舰队象征(3级)：增加自身携带的导弹装备12点火力值，全队舰船导弹战和闭幕导弹阶段受到的伤害降低50%。"""


class Skill_112992_1(CommonSkill):
    """增加自身携带的导弹装备12点火力值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=Missile)
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
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=(FirstMissilePhase, SecondMissilePhase),
                value=-0.5
            )
        ]


skill = [Skill_112992_1, Skill_112992_2]
