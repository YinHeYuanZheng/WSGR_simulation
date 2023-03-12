# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 埃克赛特改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身每损失5%耐久，增加自身12%暴击伤害。
自身攻击敌方战列、战巡、重巡时额外增加20%暴击率。"""


class Skill_112391_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            HealthBasedBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0,
                bias_or_weight=0
            ),
            AtkBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            )
        ]


class HealthBasedBuff(CoeffBuff):
    def change_value(self, *args, **kwargs):
        total_health = self.master.status['standard_health']
        health = self.master.status['health']
        loss_health_rate = 1 - health / total_health
        self.value = loss_health_rate // 0.05 * 0.12


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (BB, BC, CA))


name = '绝境求生'
skill = [Skill_112391_1]
