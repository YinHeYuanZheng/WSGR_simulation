# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 对空直卫: 秋月改-1、凉月改-1

from src.wsgr.formulas import TorpedoAtk
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""加自身及相邻船只对空值8点，自身鱼雷暴击率增加15%。"""


class Skill_111641_1(Skill):
    """加自身及相邻船只对空值8点"""
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
                name='antiair',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            ),
        ]


class Skill_111641_2(Skill):
    """自身鱼雷暴击率增加15%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.15,
                bias_or_weight=0,
                atk_request=[ATK_Request1],
            )
        ]


class ATK_Request1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, TorpedoAtk)


name = '对空直卫'
skill = [Skill_111641_1, Skill_111641_2]
