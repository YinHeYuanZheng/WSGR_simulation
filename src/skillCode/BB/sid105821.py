# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# H43-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身炮击战阶段被攻击概率提高30%。
自身炮击攻击优先攻击位置排在前方的敌方主力舰。
自身每损失1点耐久值，炮击攻击时便会增加2点额外伤害。
全队G国舰船攻击时增加其自身25%耐久值的额外伤害。"""


class Skill_105821_1(Skill):
    """自身炮击战阶段被攻击概率提高30%。
    自身炮击攻击优先攻击位置排在前方的敌方主力舰。
    自身每损失1点耐久值，炮击攻击时便会增加2点额外伤害。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MagnetBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=0.3
            ),
            PriorTargetBuff(
                timer=timer,
                name='prior_type_target',
                phase=ShellingPhase,
                target=TypeTarget(side=0, shiptype=MainShip),
                ordered=True
            ),
            WoundExtraDamage(
                timer=timer,
                name='extra_damage',
                phase=ShellingPhase,
                value=0,
                bias_or_weight=0
            )
        ]


class WoundExtraDamage(CoeffBuff):
    def change_value(self, *args, **kwargs):
        extra_damage = (self.master.status['standard_health'] -
                        self.master.status['health']) * 2
        self.value = extra_damage


class Skill_105821_2(Skill):
    """全队G国舰船攻击时增加其自身25%耐久值的额外伤害。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='G')
        self.buff = [
            HealthExtraDamage(
                timer=timer,
                name='extra_damage',
                phase=ShellingPhase,
                value=0.25,
                bias_or_weight=0
            )
        ]


class HealthExtraDamage(AtkBuff):
    def change_value(self, *args, **kwargs):
        health = self.master.status['standard_health']
        self.value = np.ceil(health * 0.25)


name = '末日狂想曲'
skill = [Skill_105821_1, Skill_105821_2]
