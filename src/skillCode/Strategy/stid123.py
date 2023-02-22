# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 过穿

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""在炮击战阶段，自身受到战列舰的伤害减少2%/4%/6%/8%。"""


class Strategy_123(SelfStrategy):
    def __init__(self, timer, master, level=3):
        super().__init__(timer, master, level)
        value = [-0.02, -0.04, -0.06, -0.08]
        self.stid = '123'
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=ShellingPhase,
                value=value[self.level],
                atk_request=[ATKRequest_1]
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.atk_body, BB)


skill = [Strategy_123]
