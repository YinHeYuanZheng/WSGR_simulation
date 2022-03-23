# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 内华达、俄克拉荷马

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
from src.wsgr.formulas import *
"""重点防御(3级)：所有阶段受到攻击时，50%概率发动，减免50%伤害，并且此次攻击不会被暴击。
"""


class Skill_110111(Skill):
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
        ]

    def activate(self, friend, enemy):
        buff = [
            SpecialBuff(
                self.timer,
                name='must_not_crit',
                phase=AllPhase,
            ),
            FinalDamageBuff(
                self.timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-0.5,
            )
        ]
        tmp_rate = np.random.random()
        if tmp_rate <= 0.5:
            self.master.add_buff(buff)


skill = [Skill_110111]
