# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 英王乔治五世-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""攻击装甲大于50点的目标时，有35%概率造成1.4倍伤害。"""


class Skill_103051(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master=master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.4,
                atk_request=[BuffRequest_1],
                rate=0.35
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
       return self.atk.target.get_final_status(name='armor') > 50


skill = [Skill_103051]
