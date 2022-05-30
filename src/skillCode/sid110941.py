# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 基阿特

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.equipment import *

"""驾束制导(3级)：提高自身携带导弹和发射架类装备10点火力值，
随机降低三名敌方单位15回避值、命中值、火力值和装甲值，对位敌人不参与首轮炮击。"""


class Skill_110941_1(CommonSkill):
    """提高自身携带导弹和发射架类装备10点火力值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=(AntiMissile, Launcher))
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
        self.target = RandomTarget(side=0, num=3)
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


class Skill_110941_3(Skill):
    """对位敌人不参与首轮炮击"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=0, loc=[self.master.loc])
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='not_act_phase',
                phase=FirstShellingPhase
            )
        ]


skill = [Skill_110941_1, Skill_110941_2, Skill_110941_3]
