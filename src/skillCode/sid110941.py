# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 基阿特

"""驾束制导(3级)：提高自身携带导弹和发射架类装备10点火力值，随机降低三名敌方单位15回避值、命中值、火力值和装甲值，对位敌人不参与首轮炮击。"""

from src.wsgr.equipment import *
from src.wsgr.phase import *
from src.wsgr.skill import *


class Skill_110941_1(Skill):
    """提高自身携带导弹和发射架类装备10点火力值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=(Missile, Launcher))
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_110941_2(Skill):
    """随机降低三名敌方单位15回避值、命中值、火力值和装甲值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target_2(side=0)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            )
        ]


class Target_2(Target):
    def get_target(self, friend, enemy):
        target = super().get_target(friend, enemy)
        if len(target) > 3:
            target = np.random.choice(target, 3, replace=False)
        return target


class Skill_110941_3(Skill):
    """对位敌人不参与首轮炮击"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target_3(master)
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='not_act_phase',
                phase=FirstShellingPhase
            )
        ]


class Target_3(SelfTarget):
    def get_target(self, friend, enemy):
        opposite = LocTarget(side=0, loc=[self.master.loc])\
            .get_target(friend=friend, enemy=enemy)
        return [opposite]


skill = [Skill_110941_1, Skill_110941_2, Skill_110941_3]
