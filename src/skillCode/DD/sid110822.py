# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 萤火虫改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战时，优先攻击中、大型船，攻击时无视敌方100%的护甲，同时有30%概率造成2倍伤害。"""


class Skill_110822(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=ShellingPhase,
                target=TypeTarget(side=0, shiptype=(MidShip, LargeShip)),
                ordered=False
            ),
            AtkBuff(
                timer=timer,
                name='ignore_armor',
                phase=ShellingPhase,
                value=-1,
                bias_or_weight=1,
                atk_request=[BuffRequest_1]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=1,
                atk_request=[BuffRequest_1],
                rate=0.3
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (MidShip, LargeShip))


name = '重装刺客'
skill = [Skill_110822]
