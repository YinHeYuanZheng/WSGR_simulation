# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 吕贝克改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身15点索敌值和10点回避值。降低敌方潜水艇12点回避值。
队伍中每有一艘G国护卫舰，全队护卫舰造成的伤害提高6%。"""


class Skill_115171_1(CommonSkill):
    """增加自身15点索敌值和10点回避值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
        ]


class Skill_115171_2(Skill):
    """降低敌方潜水艇12点回避值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=0, shiptype=SS)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-12,
                bias_or_weight=0
            )
        ]


class Skill_115171_3(Skill):
    """队伍中每有一艘G国护卫舰，全队护卫舰造成的伤害提高6%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=CoverShip)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.06
            )
        ]

    def activate(self, friend, enemy):
        g_cover = CombinedTarget(
            side=1,
            target_list=[CountryTarget(side=1, country='G'),
                         TypeTarget(side=1, shiptype=CoverShip)]
        ).get_target(friend, enemy)
        num = len(g_cover)
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= num
                tmp_target.add_buff(tmp_buff)


name = '和平卫士'
skill = [Skill_115171_1, Skill_115171_2, Skill_115171_3]
