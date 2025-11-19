# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 希佩尔海军上将-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110361(Skill):
    """伪装奇袭(3级)：炮击战时30%概率发动，攻击敌舰队中的驱逐舰且必定命中。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            SpecialAtkBuff(
                timer=timer,
                phase=ShellingPhase,
                rate=0.3,
                target=TypeTarget(side=0, shiptype=DD),
                coef={'must_hit': True}
            )
        ]


name = '伪装奇袭'
skill = [Skill_110361]
