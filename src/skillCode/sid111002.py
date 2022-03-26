# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 狮-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""单纵阵时增加我方全体战列15点装甲值，
梯形阵时增加我方全体战巡12点闪避值和命中值，
敌方主力舰>=3时增加我方全体20%暴击伤害。
当自身不为旗舰时，单纵阵增加自身20点火力值，
梯形阵增加自身20%暴击率，
敌方主力舰>=3时增加自身25点装甲值。
当自身为旗舰时增加20点火力值、25点装甲、12点命中值和闪避值、20%暴击率和暴击伤害。"""


class Skill_111002_1(Skill):
    """单纵阵时增加我方全体战列15点装甲值"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = TypeTarget(side=1, shiptype=BB)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 1


class Skill_111002_2(Skill):
    """梯形阵时增加我方全体战巡12点闪避值和命中值"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = TypeTarget(side=1, shiptype=BC)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_form() == 4


class Skill_111002_3(Skill):
    """敌方主力舰>=3时增加我方全体20%暴击伤害。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.request = [Request_1]
        self.target = Target(side=1)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]


class Skill_111002_4(Skill):
    """当自身不为旗舰时，单纵阵增加自身20点火力值，"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc != 1 and \
               self.master.get_form() == 1


class Skill_111002_5(Skill):
    """当自身不为旗舰时，梯形阵增加自身20%暴击率，"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc != 1 and \
               self.master.get_form() == 4


class Skill_111002_6(Skill):
    """当自身不为旗舰时，敌方主力舰>=3时增加自身25点装甲值。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            )
        ]
        self.request = [Request_1]

    def is_active(self, friend, enemy):
        return self.master.loc != 1 and \
               bool(self.request[0](self.timer, self.master, friend, enemy))


class Skill_111002_7(Skill):
    """当自身为旗舰时增加20点火力值、25点装甲、12点命中值和闪避值、20%暴击率和暴击伤害。"""
    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=25,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=12,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit-coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc == 1


class Request_1(Request):
    def __bool__(self):
        target = TypeTarget(
            side=0,
            shiptype=MainShip
        ).get_target(self.friend, self.enemy),
        number = len(target)
        return number >= 3


skill = [Skill_111002_1, Skill_111002_2, Skill_111002_3, Skill_111002_4,
         Skill_111002_5, Skill_111002_6, Skill_111002_7]
