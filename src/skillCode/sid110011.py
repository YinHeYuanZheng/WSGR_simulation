# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 胡德-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身作为旗舰时，为队伍中所有舰船附加 10% 的被暴击率，
为队伍中的E国舰船附加 20% 的暴击率，为其他国家的舰船附加 10% 的暴击率。"""


class Skill_110011(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='be_crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            # 暴击率，E国船两倍
            buff0 = copy.copy(self.buff[0])
            if tmp_target.status['country'] == 'E':
                buff0.value *= 2
            tmp_target.add_buff(buff0)

            # 被暴击率
            buff1 = copy.copy(self.buff[1])
            tmp_target.add_buff(buff1)


skill = [Skill_110011]
