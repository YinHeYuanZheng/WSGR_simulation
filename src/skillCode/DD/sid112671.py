# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 岛风改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身装备的鱼雷装备的鱼雷值提高100%。
自身可在先制鱼雷阶段发射队伍中J国驱逐舰数量的鱼雷（最多3枚）。
自身为舰队旗舰时，全队J国护卫舰伤害提高30%，回避率提高12%。
自身不为舰队旗舰时，自身暴击伤害提高50%，攻击威力不会因耐久损伤而降低。"""


class Skill_112671_1(CommonSkill):
    """自身装备的鱼雷装备的鱼雷值提高100%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=Torpedo)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=1,
                bias_or_weight=1
            )
        ]


class Skill_112671_2(Skill):
    """自身可在先制鱼雷阶段发射队伍中J国驱逐舰数量的鱼雷（最多3枚）"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MultipleTorpedoAtkBuff(
                timer=timer,
                name='multi_torpedo_attack',
                phase=FirstTorpedoPhase,
                num=1,
                rate=1,
            ),
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=FirstTorpedoPhase
            )
        ]

    def activate(self, friend, enemy):
        buff0 = copy.copy(self.buff[0])
        target_JDD = CombinedTarget(
                side=1,
                target_list=[TypeTarget(side=1, shiptype=DD),
                             CountryTarget(side=1, country='J')]
            ).get_target(friend, enemy)
        if self.master in target_JDD:
            target_JDD.remove(self.master)

        buff0.num = min(2, len(target_JDD))
        self.master.add_buff(buff0)

        buff1 = copy.copy(self.buff[1])
        self.master.add_buff(buff1)


class Skill_112671_3(Skill):
    """自身为舰队旗舰时，全队J国护卫舰伤害提高30%，回避率提高12%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
                side=1,
                target_list=[TypeTarget(side=1, shiptype=CoverShip),
                             CountryTarget(side=1, country='J')]
            )
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.3
            ),
            CoeffBuff(
                timer=timer,
                name='miss_rate',
                phase=AllPhase,
                value=0.12,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


class Skill_112671_4(Skill):
    """自身不为舰队旗舰时，自身暴击伤害提高50%，攻击威力不会因耐久损伤而降低。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.5,
                bias_or_weight=0
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase,
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc != 1


name = '灿若星芒'
skill = [Skill_112671_1, Skill_112671_2, Skill_112671_3, Skill_112671_4]
