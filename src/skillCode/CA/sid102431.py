# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 得梅因-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""八英寸机关枪(3级)：提升自身暴击伤害20%，炮击战阶段，有30%概率造成1.3倍的伤害。（暴击与倍率伤害不同时触发）"""


class Skill_102431(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.3,
                atk_request=[ATKRequest_1],
                rate=0.3
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return not self.atk.coef['crit_flag']


name = '八英寸机关枪'
skill = [Skill_102431]
