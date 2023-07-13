# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 天城-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身优先攻击战巡，攻击战巡时命中率提高20%，造成的伤害提升25%。自身炮击战阶段攻击命中过的敌人无法行动。
当赤城位于队伍中时，全队航母、装母、轻母造成的伤害提升10%，全队J国舰船造成的伤害提升10%。"""


class Skill_101891_1(Skill):
    """自身优先攻击战巡，攻击战巡时命中率提高20%，造成的伤害提升25%。
    自身炮击战阶段攻击命中过的敌人无法行动。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=AllPhase,
                target=TypeTarget(side=0, shiptype=BC),
                ordered=False
            ),
            AtkBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0,
                atk_request=[BuffRequest_1]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.25,
                atk_request=[BuffRequest_1]
            ),
            AtkHitBuff(
                timer=timer,
                name='atk_hit',
                phase=ShellingPhase,
                buff=[
                    ActPhaseBuff(
                        timer=timer,
                        name='not_act_phase',
                        phase=AllPhase
                    )
                ],
                side=0
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, BC)


class Skill_101891_2(Skill):
    """当赤城位于队伍中时，全队航母、装母、轻母造成的伤害提升10%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.request = [Request_1]
        self.target = TypeTarget(side=1, shiptype=(CV, AV, CVL))
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.1
            )
        ]


class Skill_101891_3(Skill):
    """当赤城位于队伍中时，全队J国舰船造成的伤害提升10%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.request = [Request_1]
        self.target = CountryTarget(side=1, country='J')
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.1
            )
        ]


class Request_1(Request):
    def __bool__(self):
        if isinstance(self.friend, Fleet):
            friend = self.friend.ship
        else:
            friend = self.friend
        for tmp_ship in friend:
            # 赤城cid = 10022/11022
            if tmp_ship.cid == '10022' or tmp_ship.cid == '11022':
                return True
        return False


name = '协调轰击'
skill = [Skill_101891_1, Skill_101891_2, Skill_101891_3]
