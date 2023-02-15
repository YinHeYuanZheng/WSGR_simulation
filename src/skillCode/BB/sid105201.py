# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 蒙大拿-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


"""炮击战阶段自身免疫受到的第一次攻击。
当敌方主力舰≥5时，增加全体舰船10%暴击率和增加自身20%暴击伤害，自身攻击必定命中（Lv.3）。"""


class Skill_105201_1(Skill):
    """炮击战阶段自身免疫受到的第一次攻击。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='shield',
                phase=ShellingPhase,
                exhaust=1
            ),
        ]


class Skill_105201_2(Skill):
    """当敌方主力舰≥5时，增加全体舰船10%暴击率"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.request = [Request_1]
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]


class Skill_105201_3(Skill):
    """当敌方主力舰≥5时，增加自身20%暴击伤害，自身攻击必定命中。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.request = [Request_1]
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.2,
                bias_or_weight=0
            ),
            SpecialBuff(
                timer=timer,
                name='must_hit',
                phase=AllPhase
            )
        ]


class Request_1(Request):
    def __bool__(self):
        target = TypeTarget(side=0,
                            shiptype=MainShip
                            ).get_target(self.friend, self.enemy)
        return len(target) >= 5


name = '舰队核心'
skill = [Skill_105201_1, Skill_105201_2, Skill_105201_3]
