# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 声望最后的荣耀

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""根据战斗点距离起始点的位置提升自身战斗力，离初始点越远战斗力越高，
每层火力、装甲、对空、命中、回避增加 3 点，
暴击率提升 3%（演习、战役、决战、立体强袭、模拟演习为5层满）。
"""
class Skill_110181_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        #target 在 activate 处体现
        self.buff = [
            StatusBuff(timer=timer,
                name="fire",
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(timer=timer,
                name="armor",
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(timer=timer,
                name="accuracy",
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(timer=timer,
                name="antiair",
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(timer=timer,
                name="evasion",
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            CoeffBuff(timer=timer,
                name="crit",
                phase=AllPhase,
                value=0.03,
                bias_or_weight=0
            )
        ]
    def activate(self, friend, enemy):
        for buff in self.buff:
            this_buff = copy.copy(buff)
            this_buff.value*=self.timer.get_dist()
            """Todo:
                特判掉强制 5 层的
                需要预留接口
            """
            self.master.add_buff(this_buff)

skill = [Skill_110181_1]
