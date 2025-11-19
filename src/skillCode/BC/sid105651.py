# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 塞瓦斯托波尔-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身攻击敌方护卫舰时命中率提高15%，伤害提高30%。
自身免疫战巡、重巡、轻巡的攻击。"""


class Skill_105651_1(Skill):
    """自身攻击敌方护卫舰时命中率提高15%，伤害提高30%。
    自身免疫战巡、重巡、轻巡的攻击。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=.15,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=.3,
                atk_request=[BuffRequest_1]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-1.,
                atk_request=[BuffRequest_2]
            ),
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, CoverShip)


class BuffRequest_2(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.atk_body, (BC, CA, CL))


name = '巡洋舰杀手'
skill = [Skill_105651_1]
