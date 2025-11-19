# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# CNT巡洋舰改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""(自身处于舰队时远征大成功率提高3%/6%/9%。)
全队舰船命中率提高9%。
自身攻击小型船时命中率提高15%，伤害提高30%。"""


class Skill_115271_1(Skill):
    """全队舰船命中率提高9%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.09,
                bias_or_weight=0
            )
        ]


class Skill_115271_2(Skill):
    """自身攻击小型船时命中率提高15%，伤害提高30%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0,
                atk_request=[AtkRequest_1]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.3,
                atk_request=[AtkRequest_1]
            ),
        ]


class AtkRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, SmallShip)


name = '蒙法尔科内旧梦'
skill = [Skill_115271_1, Skill_115271_2]
