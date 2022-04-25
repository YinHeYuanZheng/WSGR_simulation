# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 斯佩伯爵海军上将 河口之战

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战时 20% 概率发动，攻击 2 个目标，若目标是中型或小型船只，造成 120% 的伤害。
"""
class Skill_111302_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target=SelfTarget(master)
        self.buff = [
            MultipleAtkBuff(timer=timer,
                phase=ShellingPhase,
                name="multi_attack",
                num=2,
                rate=0.2,
                during_buff=[FinalDamageBuff(timer=timer,
                        name="final_damage_buff",
                        phase=ShellingPhase,
                        value=0.2,
                        atk_request=Request_1
                    )
                ],
            ),
            
        ]
class Request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target,MidShip) or \
        isinstance(self.atk.target,SmallShip)
skill = [Skill_111302_1]
