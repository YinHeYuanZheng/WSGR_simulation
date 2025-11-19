# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 但丁-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""但丁会随机选择2艘敌方舰船，降低其50%的命中值并提高其50%被暴击率。
当舰队旗舰为I国舰船时，全队航速低于27节的舰船在反航战和T劣势时攻击力不会受到航向的影响。"""


class Skill_115322_1(Skill):
    """但丁会随机选择2艘敌方舰船，降低其50%的命中值并提高其50%被暴击率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = RandomTarget(side=0, num=2)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-0.5,
                bias_or_weight=1
            ),
            CoeffBuff(
                timer=timer,
                name='be_crit',
                phase=AllPhase,
                value=0.5,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.cid in ['10532', '11532']


class Skill_115322_2(Skill):
    """当舰队旗舰为I国舰船时，全队航速低于27节的舰船在反航战和T劣势时攻击力不会受到航向的影响。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = StatusTarget(
            side=1,
            status_name='speed',
            fun='lt',
            value=27
        )
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_dir_coef',
                phase=AllPhase,
            )
        ]

    def is_active(self, friend, enemy):
        leader = friend.ship[0]
        return leader.status['country'] == 'I' and \
               self.master.get_dir_flag() in [3, 4]


name = '纵队轰击'
skill = [Skill_115322_1, Skill_115322_2]
