# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 阿拉斯加

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""先锋(3级)：炮击命中敌方航速大于等于27的单位时造成额外15点固定伤害。
自身相邻上下单位开闭幕导弹、航空战时所受到的伤害降低20%。"""


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
                atk_request=[BuffRequest_1],
                bias_or_weight=0
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
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=(FirstMissilePhase, SecondMissilePhase, AirPhase),
                value=-0.2
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.get_final_status('speed') >= 27


name = '先锋'
skill = [Skill_110201_1, Skill_110201_2]
