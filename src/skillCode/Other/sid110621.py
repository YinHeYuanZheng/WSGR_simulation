# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 火力支援(罗伯茨改-1、阿贝克隆比改-1)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加火力值25%，命中值10点，航速越低增加幅度越高，最多增加火力值50%，命中值20点。"""


class Skill_110621_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=0.25,
                bias_or_weight=2
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
        ]

    def activate(self, friend, enemy):
        re_speed = 1 - self.master.get_final_status('speed') / 12.2
        re_speed = max(0, re_speed)
        re_speed = min(1, re_speed)
        re_speed += 1
        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            tmp_buff.value *= re_speed
            self.master.add_buff(tmp_buff)


name = '火力支援'
skill = [Skill_110621_1]
