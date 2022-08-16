# -*- coding: utf-8 -*-
# Author:银河远征
# env:py38
# 海伦娜改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""六英寸机关炮(3级)：夜战时25%概率发动，对3个目标造成50%的伤害。"""


class Skill_110592(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MultipleAtkBuff(
                timer=timer,
                name='multi_attack',
                phase=NightPhase,
                num=3,
                rate=0.25,
                during_buff=[
                    FinalDamageBuff(
                        timer=timer,
                        name='final_damage_buff',
                        phase=NightPhase,
                        value=-0.5
                    )
                ]
            )
        ]


name = '六英寸机关炮'
skill = [Skill_110592]
