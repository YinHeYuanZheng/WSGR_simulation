# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 昆西-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110402(Skill):
    """旗舰杀手(3级)：炮击战30%概率发动，攻击对方舰队旗舰，增加15点固定伤害且必定命中。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff(
                timer=timer,
                name='special_attack',
                phase=ShellingPhase,
                rate=0.3,
                during_buff=[
                    CoeffBuff(
                        timer=timer,
                        name='extra_damage',
                        phase=ShellingPhase,
                        value=15,
                        bias_or_weight=0
                    )
                ],
                target=LocTarget(side=0, loc=[0]),
                coef={'must_hit': True}
            )
        ]


skill = [Skill_110402]
