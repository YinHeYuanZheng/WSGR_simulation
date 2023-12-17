# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# T23改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身编队相邻左边一艘G国小型船全阶段免疫2次伤害，
自身编队相邻右边一艘G国小型船攻击时无视敌方100%装甲值，暴击率提升20%。
当队伍里G国驱逐舰数量≥3时，全队G国驱逐舰可参与先制鱼雷攻击。"""


class Skill_115031_1(Skill):
    """自身编队相邻左边一艘G国小型船全阶段免疫2次伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                NearestLocTarget(
                    side=1,
                    master=master,
                    radius=1,
                    direction='up',
                    shiptype=SmallShip
                ),
                CountryTarget(
                    side=1,
                    country='G'
                )
            ]
        )
        self.buff = [
            DamageShield(
                timer=timer,
                phase=AllPhase,
                exhaust=2
            )
        ]


class Skill_115031_2(Skill):
    """自身编队相邻右边一艘G国小型船攻击时无视敌方100%装甲值，暴击率提升20%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                NearestLocTarget(
                    side=1,
                    master=master,
                    radius=1,
                    direction='down',
                    shiptype=SmallShip
                ),
                CountryTarget(
                    side=1,
                    country='G'
                )
            ]
        )
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='ignore_armor',
                value=-1,
                phase=AllPhase,
                bias_or_weight=1
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                value=0.2,
                phase=AllPhase,
                bias_or_weight=0
            ),
        ]


class Skill_115031_3(Skill):
    """当队伍里G国驱逐舰数量≥3时，全队G国驱逐舰可参与先制鱼雷攻击。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                TypeTarget(
                    side=1,
                    shiptype=DD
                ),
                CountryTarget(
                    side=1,
                    country='G'
                )
            ]
        )
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=FirstTorpedoPhase
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        if len(target) < 3:
            return
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_target.add_buff(tmp_buff)


name = '七岛功臣'
skill = [Skill_115031_1, Skill_115031_2, Skill_115031_3]