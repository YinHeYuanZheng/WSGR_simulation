# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 加里波第

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""北极星威慑(3级)：炮击战阶段自身命中过的目标不再行动(限炮击战阶段)。
    炮击战阶段有70%概率增加最小30%，最多100%的额外伤害。本角色无法装备大口径主炮。"""


class Skill_114131_1(Skill):
    """炮击战阶段自身命中过的目标不再行动(限炮击战阶段)"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=ShellingPhase,
                buff=[
                    ActPhaseBuff(
                        timer=timer,
                        name='not_act_phase',
                        phase=ShellingPhase
                    )
                ],
                side=0
            )
        ]


class Skill_114131_2(Skill):
    """炮击战阶段有70%概率增加最小30%，最多100%的额外伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            RandomFinalDamage(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0,
                rate=0.7
            )
        ]


class RandomFinalDamage(FinalDamageBuff):
    def change_value(self, *args, **kwargs):
        self.value = np.random.uniform(0.3, 1.)


name = '北极星威慑'
skill = [Skill_114131_1, Skill_114131_2]


