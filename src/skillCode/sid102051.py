# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 约克公爵-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

"""骑士之誓(3级)：队伍中每有一艘非E国的船只都会增加自身命中、回避、火力3点。
"""


class Skill_102051(Skill):
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target_not_e = NotTagTarget(
            side=1,
            tag_name='country',
            tag='E'
        ).get_target(friend, enemy)

        buff_num = len(target_not_e)
        for tmp_buff in self.buff[:]:
            tmp_buff.value *= buff_num
            self.master.add_buff(tmp_buff)


skill = [Skill_102051]
