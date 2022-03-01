# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# G6-1

import numpy as np
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""航空战阶段增加自身40点制空值。
全阶段队伍中随机3艘J国舰船增加10点火力值，对敌方造成的伤害提高15%"""


class Skill_104941_1(Skill):
    """航空战阶段增加自身40点制空值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_con_buff',
                phase=(AirPhase,),
                value=40,
                bias_or_weight=0
            )
        ]


class Skill_104941_2(Skill):
    """全阶段队伍中随机3艘J国舰船增加10点火力值，对敌方造成的伤害提高15%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = StatusTarget(
            side=1,
            status_name='country',
            fun='eq',
            value='J',
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.15
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        if len(target) > 3:
            target = np.random.choice(target, 3, replace=False)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_target.add_buff(tmp_buff)


skill = [Skill_104941_1, Skill_104941_2]
