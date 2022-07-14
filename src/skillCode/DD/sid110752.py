# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# Z16改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""提升自身16点鱼雷值。
鱼雷战时，有30%概率额外发射1枚鱼雷，概率触发时所有鱼雷造成的伤害提升30%；
每有一艘Z系驱逐提高12%发动概率。"""


class Skill_110752_1(CommonSkill):
    """提升自身16点鱼雷值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=16,
                bias_or_weight=0
            )
        ]


class Skill_110752_2(Skill):
    """鱼雷战时，有30%概率额外发射1枚鱼雷，概率触发时所有鱼雷造成的伤害提升30%；
    每有一艘Z系驱逐提高12%发动概率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff_z16(
                timer=timer,
                name='multi_attack',
                phase=SecondTorpedoPhase,
                rate=.3,
            )
        ]

    def activate(self, friend, enemy):
        zship = TagTarget(side=1, tag='z-ship').get_target(friend, enemy)
        buff0 = copy.copy(self.buff[0])
        buff0.rate = min(1., buff0.rate + 0.12 * len(zship))
        self.master.add_buff(buff0)


class SpecialBuff_z16(SpecialBuff):
    """概率触发时所有鱼雷造成的伤害提升30%"""
    def activate(self, *args, **kwargs):
        buff0 = FinalDamageBuff(
            timer=self.timer,
            name='final_damage_buff',
            phase=SecondTorpedoPhase,
            value=0.3
        )
        self.master.add_buff(buff0)


name = '连环爆破'
skill = [Skill_110752_1, Skill_110752_2]
