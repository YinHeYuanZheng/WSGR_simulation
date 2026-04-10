# -*- coding:utf-8 -*-
# Author:huan_yp
# Edited by: 银河远征(20260410)
# env:py38
# 空想

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""高速机动(3级)：自身被攻击概率提高20%，受到攻击时50%概率免疫所有伤害。
自身每受到一次攻击，自身命中率、回避率、暴击率提高5%。"""


class Skill_110991(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.2,
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-1,
                rate=0.5
            ),
            AtkHitBuff(
                timer=timer,
                name='get_atk',
                phase=AllPhase,
                buff=[
                    CoeffBuff(
                        timer=timer,
                        name='hit_rate',
                        phase=AllPhase,
                        value=0.05,
                        bias_or_weight=0
                    ),
                    CoeffBuff(
                        timer=timer,
                        name='miss_rate',
                        phase=AllPhase,
                        value=0.05,
                        bias_or_weight=0
                    ),
                    CoeffBuff(
                        timer=timer,
                        name='crit',
                        phase=AllPhase,
                        value=0.05,
                        bias_or_weight=0
                    ),
                ],
                side=1
            )
        ]


name = '高速机动'
skill = [Skill_110991]
