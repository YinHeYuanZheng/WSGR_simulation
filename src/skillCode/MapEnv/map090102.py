# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 9图封锁战况(削弱后)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_090102_1(PrepSkill):
    """敌方舰队旗舰存活时，为所有非旗舰单位提供10%减伤"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = LocTarget(side=0, loc=[2,3,4,5,6])
        self.buff = [
            LeaderSurviveBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-0.1
            )
        ]


class LeaderSurviveBuff(FinalDamageBuff):
    def is_active(self, *args, **kwargs):
        leader = self.master.master.ship[0]
        return leader.damaged <= 3


name = '9图封锁战况(削弱后)'
effect = '敌方舰队旗舰存活时，为所有非旗舰单位提供10%减伤'
skill = [NormalMap_090102_1]
