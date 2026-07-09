# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 卡拉乔洛改

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队I国舰船航速增加5节，回避值和火力值增加15点。
敌方航速27节及以下的舰船命中率和伤害降低20%，
我方航速27节及以上的舰船命中率和伤害提高20%。"""


class Skill_115831_1(PrepSkill):
    """全队I国舰船航速增加5节"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='I')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='speed',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


class Skill_115831_2(Skill):
    """全队I国舰船回避值和火力值增加15点"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='I')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_115831_3(Skill):
    """敌方航速27节及以下的舰船命中率和伤害降低20%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = StatusTarget(
            side=0, status_name='speed', fun='le', value=27
        )
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=-0.2,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=-0.2
            )
        ]


class Skill_115831_4(Skill):
    """我方航速27节及以上的舰船命中率和伤害提高20%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = StatusTarget(
            side=1, status_name='speed', fun='ge', value=27
        )
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.2
            )
        ]


name = '圣翼裁決'
skill = [Skill_115831_1, Skill_115831_2, Skill_115831_3, Skill_115831_4]
