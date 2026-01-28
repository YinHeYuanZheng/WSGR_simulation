# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 谦逊改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from AADG_common import *

"""自身攻击小型船时，命中率和伤害提高20%。
全队S国护卫舰火力值和回避值增加15点。
提高自身携带的导弹装备8点火力值，自身装备的发射器会视为反潜装备，其索敌值视为对潜值。
当敌方存在航母时，全队回避值和对空值增加20点。"""


class Skill_115091_1(Skill):
    """自身攻击小型船时，命中率和伤害提高20%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0,
                atk_request=[AtkRequest_1]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.2,
                atk_request=[AtkRequest_1]
            ),
        ]


class AtkRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, SmallShip)


class Skill_115091_2(Skill):
    """全队S国护卫舰火力值和回避值增加15点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[CountryTarget(side=1, country='S'),
                         TypeTarget(side=1, shiptype=CoverShip)]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
        ]


class Skill_115091_3(CommonSkill):
    """提高自身携带的导弹装备8点火力值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=Missile)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            )
        ]


class Skill_115091_4(CommonSkill):
    """当敌方存在航母时，全队回避值和对空值增加20点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
        ]

    def is_active(self, friend, enemy):
        target = TypeTarget(side=0, shiptype=CV
                            ).get_target(friend, enemy)
        return len(target)


name = '远航'
skill = [Skill_115091_1, Skill_115091_2, Skill_115091_3,
         Skill_115091_4, AADGCommonSkill]
