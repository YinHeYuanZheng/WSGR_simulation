# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 斯大林格勒

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""huan_yp:
write in 2022.4.24
recheck in 2022.4.25

"""

"""
增加自身火力值 10 点，
降低自身命中值 5 点。
炮击战阶段该舰命中的目标是非满血状态，则增加10%/15%/20%额外伤害，
次轮炮击战阶段自身被命中时，减少10%/15%/20%受到的伤害。
"""

class Skill_103971_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target=SelfTarget(master)
        self.buff=[
            CommonBuff(timer=timer,
                name="fire",
                phase=[AllPhase],
                value=10,
                bias_or_weight=0
            ),
            CommonBuff(timer=timer,
                name="accuracy",
                phase=[AllPhase],
                value=-5,
                bias_or_weight=0
            ),
            FinalDamageBuff(timer=timer,
                name="final_damage_buff",
                phase=[ShellingPhase],
                value=0.2,
                bias_or_weight=2,
                atk_request=[Request_1],
            ),
            FinalDamageBuff(timer=timer,
                name="final_damage_debuff",
                phase=[SecondShellingPhase],
                bias_or_weight=2,
                value=-0.2,
            )

        ]
class Request_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.get_final_status(name="health") != self.atk.target.get_final_status(name="total_health")
skill=[Skill_103971_1]