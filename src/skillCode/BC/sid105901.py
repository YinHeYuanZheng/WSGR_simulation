# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 金伯恩-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队舰船回避值增加9点。
炮击战阶段自身优先攻击位置排在前方的敌方航母、装母、战列、战巡。
自身攻击敌方大型船时额外提高15%伤害和15%命中率。
自身攻击敌方舰队旗舰时伤害提高15%。"""


class Skill_105901_1(Skill):
    """全队舰船回避值增加9点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]


class Skill_105901_2(Skill):
    """炮击战阶段自身优先攻击位置排在前方的敌方航母、装母、战列、战巡。
    自身攻击敌方大型船时额外提高15%伤害和15%命中率。
    自身攻击敌方舰队旗舰时伤害提高15%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=ShellingPhase,
                target=TypeTarget(side=0, shiptype=(CV, AV, BB, BC)),
                ordered=True
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.15,
                atk_request=[AtkRequest_1]
            ),
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
                value=0.15,
                atk_request=[AtkRequest_2]
            ),
        ]


class AtkRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, LargeShip)


class AtkRequest_2(ATKRequest):
    def __bool__(self):
        return self.atk.target.loc == 1


name = '先锋突破'
skill = [Skill_105901_1, Skill_105901_2]
