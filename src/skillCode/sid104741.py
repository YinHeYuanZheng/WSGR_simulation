# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 72工程-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
"""增加自身15点火力值，航空战阶段优先攻击对位敌人，命中过的对位敌人在炮击战阶段无法攻击。"""


class Skill_101471_1(CommonSkill):
    """增加自身15点火力值"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                name='fire',
                phase=(AllPhase,),
                value=15,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        return True


class Skill_101471_2(Skill):
    # todo 航空战阶段优先攻击对位敌人，
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [

        ]

    def is_active(self, friend, enemy):
        return True


class Skill_101471_3(Skill):
    """命中过的对位敌人在炮击战阶段无法攻击"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                name='atk_hit',
                phase=(ShellingPhase,),
                buff=[
                    # todo 沉默
                ],
                side=0  # 敌人
            )
        ]

    def is_active(self, friend, enemy):
        return True


class Request_1(Request):
    def __bool__(self):
        pass


skill = [Skill_101471_1, Skill_101471_2, Skill_101471_3]
