# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 女灶神

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""希望的曙光(3级)：增加自身回避30点，降低自身被攻击概率30%，
战斗结束后，回复上一场战斗损失耐久最多的船只40%的在上一场的受损耐久。"""


class Skill_103071_1(CommonSkill):
    """增加自身回避30点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=30,
                bias_or_weight=0
            )
        ]


class Skill_103071_2(Skill):
    """降低自身被攻击概率30%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            UnMagnetBuff(
                timer=timer,
                phase=AllPhase,
                rate=0.3,
            )
        ]


class Skill_103071_3(EndSkill):
    """战斗结束后，回复上一场战斗损失耐久最多的船只40%的在上一场的受损耐久。"""
    def activate(self, friend, enemy):
        got_damage = 0
        target = None
        for tmp_ship in friend.ship:
            if tmp_ship.got_damage > got_damage:
                got_damage = tmp_ship.got_damage
                target = tmp_ship

        if isinstance(target, Ship):
            target.status['health'] += np.floor(0.4 * got_damage)


name = '希望的曙光'
skill = [Skill_103071_1, Skill_103071_2, Skill_103071_3]
