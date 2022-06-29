# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 星座-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""先头部队: 昼战阶段降低敌方所有战巡、战列 21 点火力值与 12 点命中值；
炮击战阶段，自身免疫航速≤27节的大型船攻击的伤害（对敌方旗舰无效），
自身命中敌方航速≥27节的舰船时增加 20% 伤害。"""


class Skill_113622_1(Skill):
    """昼战阶段降低敌方所有战巡、战列 21 点火力值与 12 点命中值；"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=(BB, BC))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=DaytimePhase,
                value=-21,
                bias_or_weight=0,
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=DaytimePhase,
                value=-12,
                bias_or_weight=0,
            )
        ]


class Skill_113622_2(Skill):
    """炮击战阶段，自身免疫航速≤27节的大型船攻击的伤害（对敌方旗舰无效），
    自身命中敌方航速≥27节的舰船时增加 20% 伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='shield',
                phase=ShellingPhase,
                atk_request=[Request_1]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.2,
                atk_request=[Request_2],
            )
        ]


class Request_1(ATKRequest):
    def __bool__(self):
        if self.atk.atk_body.loc == 1:
            return False
        return self.atk.atk_body.get_final_status('speed') <= 27 and \
               isinstance(self.atk.atk_body, LargeShip)


class Request_2(ATKRequest):
    def __bool__(self):
        return self.atk.atk_body.get_final_status('speed') >= 27


skill = [Skill_113622_1, Skill_113622_2]
