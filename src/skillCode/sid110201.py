# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 阿拉斯加

"""先锋(3级)：炮击命中敌方航速大于等于27的单位时造成额外15点固定伤害。自身相邻上下单位开闭幕导弹、航空战时所受到的伤害降低20%。"""


import numpy as np
from src.wsgr.phase import *
from src.wsgr.skill import *

class Skill_110201_1(Skill):
    """炮击命中敌方航速大于等于27的单位时造成额外15点固定伤害。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='extra_damage',
                phase=ShellingPhase,
                value=15,
                atk_request=[Request],
            )
        ]


class Skill_110201_2(Skill):
    """自身相邻上下单位开闭幕导弹、航空战时所受到的伤害降低20%。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='near'
        )
        self.buff = [
            CoeffBuff_1(
                timer=timer
            )
        ]


class Request(ATKRequest):
    def __bool__(self):
        return self.atk.atk_body.get_final_status('speed') >= 27


class CoeffBuff_1(CoeffBuff):
    def __init__(self, timer, phase=(MissilePhase, AirPhase), name='reduce_damage',
                 value=0, bias_or_weight=0, rate=1):
        super().__init__(timer, name, phase, value, bias_or_weight, rate)

    def is_active(self, damage, *args, **kwargs):
        self.value = np.floor(damage * 0.2)
        return True


skill = [Skill_110201_1, Skill_110201_2]
