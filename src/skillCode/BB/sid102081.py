# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 马萨诸塞-1

import numpy as np
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""重击(3级)：攻击有40%概率降低被命中单位75%的火力（夜战阶段无效），有35%概率造成敌方总血量20%的额外伤害。"""


class Skill_102081(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=DaytimePhase,
                buff=[
                    StatusBuff(
                        timer=timer,
                        name='fire',
                        phase=AllPhase,
                        value=-0.75,
                        bias_or_weight=1
                    )
                ],
                side=0,
                rate=0.4
            ),
            HealthExtraDamage(
                timer=timer,
                name='extra_damage',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0,
                rate=0.35
            )
        ]


class HealthExtraDamage(AtkBuff):
    def change_value(self, *args, **kwargs):
        try:
            atk = kwargs['atk']
        except:
            atk = args[0]
        self.value = np.ceil(atk.target.status['standard_health'] * 0.2)


skill = [Skill_102081]
