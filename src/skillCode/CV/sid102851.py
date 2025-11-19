# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 85工程

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队S国舰船索敌值和命中值增加6点。
索敌成功时，自身因战斗造成的舰载机损失减少100%。"""


class Skill_102851_1(PrepSkill):
    """全队S国舰船索敌值增加6点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='S')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=6,
                bias_or_weight=0,
            ),
        ]


class Skill_102851_2(Skill):
    """全队S国舰船命中值增加6点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='S')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=6,
                bias_or_weight=0,
            ),
        ]


class Skill_102851_3(Skill):
    """索敌成功时，自身因战斗造成的舰载机损失减少100%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='fall_rest',
                phase=AirPhase,
                value=-1,
                bias_or_weight=1,
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_recon_flag()


name = '舰队防空圈'
skill = [Skill_102851_1, Skill_102851_2, Skill_102851_3]
