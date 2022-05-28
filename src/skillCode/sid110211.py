# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 关岛

"""舰队防御伞(3级)：炮击战阶段，炮击会对敌方大型船单位造成额外25%的伤害。降低敌方开幕航空战与开幕导弹15%命中率。
"""

from src.wsgr.phase import *
from src.wsgr.ship import *
from src.wsgr.skill import *


class Skill_110211_1(Skill):
    """炮击战阶段，炮击会对敌方大型船单位造成额外25%的伤害。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.25,
                bias_or_weight=0,
                atk_request=(Request_1)
            )
        ]


class Request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, LargeShip)


class Skill_110211_2(Skill):
    """降低敌方开幕航空战与开幕导弹15%命中率。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=0)
        self.buff = [
            CoeffBuff(
                timer,
                name='hit_rate',
                phase=(FirstMissilePhase, AirPhase),
                value=-0.15,
                bias_or_weight=0
            )
        ]


skill = [Skill_110211_1, Skill_110211_2]
