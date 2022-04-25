# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 安森

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""队伍中每有一艘战巡都会增加自身 5% 暴击率和暴击伤害。
"""

class Skill_104841_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target=SelfTarget(master)
        self.buff=[
            CoeffBuff(timer=timer,
                name="crit",
                phase=AllPhase,
                value=0.05,
                bias_or_weight=0,
            ),
            AtkBuff(timer=timer,
                name="crit_coef",
                phase=AllPhase,
                value=0.05,
                bias_or_weight=0
            )
        ]
    def activate(self, friend, enemy):
        num = len(TypeTarget(side=1,shiptype=BC).get_target(friend,enemy))
        buff = copy.copy(self.buff[0])
        buff.value *= num
        target = self.target.get_target(friend,enemy)[0]
        target.add_buff(buff)
        
skill = [Skill_104841_1]