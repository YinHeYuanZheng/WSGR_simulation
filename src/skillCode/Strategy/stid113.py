# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 拦阻射击

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""在炮击战阶段，对驱逐舰造成的伤害增加2%/4%/6%/8%。"""


class Strategy_113(SelfStrategy):
    def __init__(self, timer, master, level=3):
        super().__init__(timer, master, level)
        value = [0.02, 0.04, 0.06, 0.08]
        self.stid = '113'
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=value[self.level],
                atk_request=[ATKRequest_1]
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, DD)


skill = [Strategy_113]
