# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 威悉河改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身舰载机威力提高20%。
队伍中每有1艘G国护卫舰，全队G国舰船回避值和对空值增加8点。
队伍中每有1艘G国主力舰，全队G国舰船火力值和装甲值增加5点。"""


class Skill_115451_1(Skill):
    """自身舰载机威力提高20%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=2
            )
        ]


class Skill_115451_2(Skill):
    """队伍中每有1艘G国护卫舰，全队G国舰船回避值和对空值增加8点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='G')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            ),
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        g_cover = TypeTarget(side=1, shiptype=CoverShip).get_target(target, None)
        if len(g_cover) == 0:
            return
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= len(g_cover)
                tmp_target.add_buff(tmp_buff)


class Skill_115451_3(Skill):
    """队伍中每有1艘G国主力舰，全队G国舰船火力值和装甲值增加5点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='G')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        g_main = TypeTarget(side=1, shiptype=MainShip).get_target(target, None)
        if len(g_main) == 0:
            return
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= len(g_main)
                tmp_target.add_buff(tmp_buff)


name = '未曾设想之路'
skill = [Skill_115451_1, Skill_115451_2, Skill_115451_3]
