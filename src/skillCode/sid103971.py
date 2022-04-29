# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 斯大林格勒-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""
增加自身火力值10点，降低自身命中值5点。
炮击战阶段该舰命中的目标是非满血状态，则增加20%额外伤害，次轮炮击战阶段自身被命中时，减少20%受到的伤害。
"""


class Skill_103971_1(CommonSkill):
    """增加自身火力值10点，降低自身命中值5点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-5,
                bias_or_weight=0
            )
        ]


class Skill_103971_2(Skill):
    """炮击战阶段该舰命中的目标是非满血状态，则增加20%额外伤害，
    次轮炮击战阶段自身被命中时，减少20%受到的伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.2,
                atk_request=[Request_1],
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=SecondShellingPhase,
                value=-0.2,
            )
        ]


class Request_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.status['health'] != \
               self.atk.target.status['standard_health']


skill = [Skill_103971_1, Skill_103971_2]
