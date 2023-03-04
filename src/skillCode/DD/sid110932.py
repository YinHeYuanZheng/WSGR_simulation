# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 基林-FRAM改造

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""装备的索敌值90%同时视为火力值和对空值。
自身耐久值高于30%最大耐久时，提升自身12%暴击率、12点鱼雷值、12点闪避值。"""


class Skill_110932_1(CommonSkill):
    """装备的索敌值90%同时视为火力值和对空值。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=.9,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=.9,
                bias_or_weight=0
            ),
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        e_recon = self.master.get_equip_status('recon')
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= e_recon
                tmp_target.add_buff(tmp_buff)


class Skill_110932_2(Skill):
    """自身耐久值高于30%最大耐久时，提升自身12%暴击率、12点鱼雷值、12点闪避值。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            HealthBasedBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            HealthBasedBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            HealthBasedBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.12,
                bias_or_weight=0
            )
        ]


class HealthBasedBuff(StatusBuff):
    def is_active(self, *args, **kwargs):
        total_health = self.master.status['standard_health']
        health = self.master.status['health']
        health_rate = health / total_health
        return isinstance(self.timer.phase, self.phase) and \
               health_rate > .3


name = 'FRAM改造'
skill = [Skill_110932_1, Skill_110932_2]
