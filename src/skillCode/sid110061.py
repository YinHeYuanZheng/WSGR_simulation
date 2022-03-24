# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 俾斯麦-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
from src.wsgr.formulas import *

"""旗舰杀手(3级)：当俾斯麦作为旗舰时，40%概率发动，攻击对方舰队旗舰并+20%穿甲，增加30点固定伤害且必定命中。
"""


class Skill_110061(Skill):
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = []

    def is_active(self, friend, enemy):
        return self.master.loc == 1

    def activate(self, friend, enemy):
        tmp_rate = np.random.random()
        buff = [
            AtkBuff(
                self.timer,
                name='pierce_coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            ),
            SpecialBuff(
                self.timer,
                name='must_hit',
                phase=AllPhase,
            ),
            PriorTargetBuff(
                self.timer,
                name='pierce_coef',
                phase=AllPhase,
                target=Target(side=0),
                ordered=True
            ),
            AtkBuff(
                self.timer,
                name='extra_damage',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            )

        ]
        if tmp_rate <= 0.4:
            self.master.add_buff(buff)


skill = [Skill_110061]
