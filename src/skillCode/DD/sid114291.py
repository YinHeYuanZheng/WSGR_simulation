# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 马伊·布雷泽改

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身可参与先制鱼雷攻击。自身攻击护卫舰时命中率和伤害提高30%。
队伍中每有一艘F国舰船，都会提高自身20%造成的伤害。"""


class Skill_114291_1(Skill):
    """自身可参与先制鱼雷攻击"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=FirstTorpedoPhase
            )
        ]


class Skill_114291_2(Skill):
    """自身攻击护卫舰时命中率和伤害提高30%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0,
                atk_request=[AtkCoverShipRequest]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.3,
                atk_request=[AtkCoverShipRequest]
            )
        ]


class AtkCoverShipRequest(ATKRequest):
    """攻击目标为护卫舰(CoverShip)"""

    def __bool__(self):
        return isinstance(self.atk.target, CoverShip)


class Skill_114291_3(Skill):
    """队伍中每有一艘F国舰船，都会提高自身20%造成的伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.2
            )
        ]

    def activate(self, friend, enemy):
        count = len(CountryTarget(side=1, country='F').get_target(friend, enemy))
        if count == 0:
            return
        buff0 = copy.copy(self.buff[0])
        buff0.value = 0.2 * count
        self.master.add_buff(buff0)


name = '进攻式护卫'
skill = [Skill_114291_1, Skill_114291_2, Skill_114291_3]
