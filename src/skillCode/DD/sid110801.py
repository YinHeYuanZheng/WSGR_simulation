# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# Z31

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""根据队伍中Z系驱逐的数量(包括自身)增加不同的能力，每多一艘额外增加一种能力，
顺序为装甲，火力，鱼雷，回避，命中，对空。增加幅度为 20%。"""


class Skill_110801_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=.2,
                bias_or_weight=1
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=.2,
                bias_or_weight=1
            ),
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=.2,
                bias_or_weight=1
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=.2,
                bias_or_weight=1
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=.2,
                bias_or_weight=1
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=.2,
                bias_or_weight=1
            ),
        ]

    def activate(self, friend, enemy):
        # 获取z驱数量
        count = len(TagTarget(side=1, tag='z-ship'
                              ).get_target(friend, enemy))
        # 根据z驱数量，依次获得效果
        for i in range(count):
            tmp_buff = copy.copy(self.buff[i])
            self.master.add_buff(tmp_buff)


name = 'Z驱菁英'
skill = [Skill_110801_1]
