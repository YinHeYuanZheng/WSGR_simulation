# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 胡德荣耀

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身作为旗舰时，为队伍中所有舰船附加 10% 的被暴击率，
为队伍中的E国舰船附加 20% 的暴击率，
为其他国家的舰船附加 10% 的暴击率。
"""


class Skill_110011_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        #target 在 activate 中体现
        self.buff = [
            CoeffBuff(timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            CoeffBuff(timer=timer,
                name='be_crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]
    def activate(self, friend, enemy):
        for target in Target(side=1).get_target(friend,enemy):
            this_buff0 = copy.copy(self.buff[0])
            if(target.status["country"] == 'E'):
                this_buff0.value *= 2
            this_buff1 = copy.copy(self.buff[1])
            target.add_buff(this_buff0)
            target.add_buff(this_buff1)

skill = [Skill_110011_1]
