# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 无比

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
"""huan_yp;
write in 2022.4.24
recheck in 2022.4.25
"""

"""自身被暴击率增加25%/20%/15%，
攻击战列，战巡、航战时，造成110%/115%/120%的伤害，
攻击航速低于自己的目标时，暴击率增加5%/10%/15%。"""

class Skill_103311_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target=SelfTarget(master)
        self.buff=[
            CoeffBuff(timer=timer,
                name='be_crit',
                phase=(AllPhase,),
                value=0.15,
                bias_or_weight=0
            ),
            FinalDamageBuff(timer=timer,
                name="final_damage_buff",
                phase=(AllPhase,),
                value=0.2,
                atk_request=[Request_1],
            ),
            AtkBuff(timer=timer,
                name="crit",
                phase=(AllPhase,),
                bias_or_weight=0,
                value=0.15,
                atk_request=[Request_2],
            ),
        ]

class Request_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target,BB) \
            or isinstance(self.atk.target,BBV) \
            or isinstance(self.atk.target,BC)
class Request_2(ATKRequest):
    def __bool__(self):
        return self.atk.target.get_final_status(name="speed") < self.atk.atk_body.get_final_status(name="speed")