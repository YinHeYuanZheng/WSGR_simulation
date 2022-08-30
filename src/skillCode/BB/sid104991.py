# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 克里蒙梭-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身攻击时降低敌人50%装甲值，并且提升敌方50%装甲值的额外伤害"""


class Skill_104991(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='ignore_armor',
                phase=AllPhase,
                value=-0.5,
                bias_or_weight=1
            ),
            AtkBuff_1(
                timer=timer,
                name='extra_damage',
                phase=AllPhase,
                value=0.5,
                bias_or_weight=0
            )
        ]


class AtkBuff_1(AtkBuff):
    def is_active(self, *args, **kwargs):
        try:
            atk = kwargs['atk']
        except:
            atk = args[0]

        self.value = np.ceil(atk.target.get_final_status('armor') * 0.5)
        return self.rate_verify()


skill = [Skill_104991]
