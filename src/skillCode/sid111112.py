# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 华盛顿-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""夜战突击(3级)：增加自身5点耐久值、15点火力值、15点装甲值和15点命中值。
夜战阶段敌方旗舰和自身对位水上目标无法行动。
夜战阶段自身攻击必定命中且必定暴击,优先攻击敌方位置排在前方的大型船。
"""


class Skill_111112_1(CommonSkill):
    """增加自身5点耐久值、15点火力值、15点装甲值和15点命中值。"""

    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='health',
                value=5,
                phase=AllPhase,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='fire',
                value=15,
                phase=AllPhase,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='armor',
                value=15,
                phase=AllPhase,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                value=15,
                phase=AllPhase,
                bias_or_weight=0
            )
        ]


class Skill_111112_2(Skill):
    """夜战阶段敌方旗舰和自身对位水上目标无法行动。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SkillTarget(master)
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name="not_act_phase",
                phase=NightPhase
            )
        ]


class SkillTarget(SelfTarget):
    def get_target(self, friend, enemy):
        lead = LocTarget(side=0, loc=[1])\
            .get_target(friend=friend, enemy=enemy)
        opposite = LocTarget(side=0, loc=[self.master.loc])\
            .get_target(friend=friend, enemy=enemy)

        target = [lead]
        if opposite != lead and not isinstance(opposite, Submarine):
            target.append(opposite)

        return target


class Skill_111112_3(Skill):
    """夜战阶段自身攻击必定命中且必定暴击,优先攻击敌方位置排在前方的大型船。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name="must_hit",
                phase=NightPhase
            ),
            SpecialBuff(
                timer=timer,
                name="must_crit",
                phase=NightPhase
            ),
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=NightPhase,
                target=OrderedTypeTarget(shiptype=(LargeShip,)),
                ordered=True
            )
        ]


skill = [Skill_111112_1, Skill_111112_2, Skill_111112_3]
