# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 新奥尔良改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""当没有受到伤害时，为自己和相邻的船只增加10点回避，当受到伤害后，自身回避+5。"""


class Skill_111431(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='near',
            master_include=True
        )

        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        # 满血状态加群体回避，并加受伤时效果
        if self.master.status['health'] == self.master.status['standard_health']:
            evsn_buff_0 = copy.copy(self.buff[0])
            target = self.target.get_target(friend, enemy)
            for tmp_target in target:
                tmp_target.add_buff(evsn_buff_0)

            evsn_buff_1 = copy.copy(self.buff[1])
            evsn_buff_1.value = 0
            self.master.add_buff(evsn_buff_1)

            after_dmg_buff = AfterDmgBuff(
                timer=self.timer,
                name='atk_be_hit',
                phase=AllPhase,
                buff=[evsn_buff_0, evsn_buff_1],
                side=1
            )
            self.master.add_buff(after_dmg_buff)

        # 受伤状态直接给自己加回避
        else:
            evsn_buff_1 = copy.copy(self.buff[1])
            self.master.add_buff(evsn_buff_1)


class AfterDmgBuff(AtkHitBuff):
    def activate(self, atk, *args, **kwargs):
        self.buff[0].value = 0
        self.buff[1].value = 5
