# -*- coding:utf-8 -*-
# Author:stars
# Edited by: 银河远征(20260410)
# env:py38
# 圣乔治-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""巨炮火力(3级)：当队伍中战列≥2时，自身火力值和装甲值增加25点，伤害提高25%；
当队伍中战巡≥2时，自身命中值和回避值增加25点，暴击率和暴击伤害提高25%。
自身攻击火力比自身低的舰船时，伤害提高30%，攻击火力比自身高的舰船时，暴击伤害提高30%。
"""


class Skill_113802_1(Skill):
    """当队伍中战列≥2时，自身火力值和装甲值增加25点，伤害提高25%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.25
            )
        ]

    def is_active(self, friend, enemy):
        target = (TypeTarget(side=1, shiptype=BB)
                  .get_target(friend, enemy))
        return len(target) >= 2


class Skill_113802_2(Skill):
    """当队伍中战巡≥2时，自身命中值和回避值增加25点，暴击率和暴击伤害提高25%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.25,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.25,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        target = (TypeTarget(side=1, shiptype=BC)
                  .get_target(friend, enemy))
        return len(target) >= 2


class Skill_113802_3(Skill):
    """攻击火力比自身低的舰船时伤害提高30%，攻击火力比自身高的舰船时暴击伤害提高30%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.3,
                atk_request=[ATKRequest_LowFire]
            ),
            AtkBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0,
                atk_request=[ATKRequest_HighFire]
            )
        ]


class ATKRequest_LowFire(ATKRequest):
    """目标火力低于自身火力"""
    def __bool__(self):
        return self.atk.target.get_final_status('fire') < \
               self.atk.source.get_final_status('fire')


class ATKRequest_HighFire(ATKRequest):
    """目标火力高于自身火力"""
    def __bool__(self):
        return self.atk.target.get_final_status('fire') > \
               self.atk.source.get_final_status('fire')


name = '巨炮火力'
skill = [Skill_113802_1, Skill_113802_2, Skill_113802_3]
