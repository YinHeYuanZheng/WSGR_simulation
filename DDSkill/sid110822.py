# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 萤火虫-重装刺客

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""
炮击战时，优先攻击中、大型船，攻击时无视敌方100%的护甲，同时有30%概率造成2倍伤害。"""
class Skill_110822_1(Skill):
    """炮击战时，优先攻击中、大型船，攻击时无视敌方100%的护甲，同时有30%概率造成2倍伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=1.0,
                name='special_attack',
                num=1,
                during_buff=[
                    CoeffBuff(
                        timer=timer,
                        name='ignore_armor',
                        phase=ShellingPhase,
                        value=-1,
                        bias_or_weight=1
                    ),
                    FinalDamageBuff(
                        timer=timer,
                        name='final_damage_buff',
                        phase=ShellingPhase,
                        value=1.0,
                        rate=.3
                    )
                ],
                target=TypeTarget(side=0, shiptype=(LargeShip, MidShip))
            )
            
        ]
            
skill = [Skill_110822_1]