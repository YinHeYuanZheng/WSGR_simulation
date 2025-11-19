# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 岚

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""爆雷奇袭(3级)：提升相当于火力值30%的鱼雷值和对潜值，
鱼雷战和夜战时，根据对手损失耐久提高暴击几率，暴击几率最少+5%，最高+30%。"""


class Skill_112651_1(CommonSkill):
    """提升相当于火力值30%的鱼雷值和对潜值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=1
            ),
            CommonBuff(
                timer=timer,
                name='antisub',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=1
            )
        ]

    def activate(self, friend, enemy):
        fire = self.master.get_final_status('fire')
        for buff in self.buff:
            this_buff = copy.copy(buff)
            this_buff.value *= fire
            self.master.add_buff(this_buff)


class Skill_112651_2(Skill):
    """鱼雷战和夜战时，根据对手损失耐久提高暴击几率，暴击几率最少+5%，最高+30%。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)

        self.buff = [
            HealthBasedBuff(
                timer=timer,
                name='crit',
                phase=(SecondTorpedoPhase, NightPhase),
                value=0.05,
                bias_or_weight=0
            )
        ]


class HealthBasedBuff(AtkBuff):
    def change_value(self, *args, **kwargs):
        try:
            atk = kwargs['atk']
        except:
            atk = args[0]
        total_health = atk.target.status['standard_health']
        health = atk.target.status['health']
        self.value = 0.05 + 0.25 * \
                     (total_health - health) / \
                     (total_health - 1)


name = '爆雷奇袭'
skill = [Skill_112651_1, Skill_112651_2]
