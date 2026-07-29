# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-5封锁战况(削弱前)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_080501_1(PrepSkill):
    """敌方舰队旗舰存活时，为所有非旗舰单位提供30%减伤"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = LocTarget(side=0, loc=[2, 3, 4, 5, 6])
        self.buff = [
            LeaderSurviveBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-0.3
            )
        ]


class LeaderSurviveBuff(FinalDamageBuff):
    def is_active(self, *args, **kwargs):
        leader = self.master.master.ship[0]
        return leader.damaged <= 3


class NormalMap_080501_2(PrepSkill):
    """航母、轻母火力-40"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=(CV, CVL))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-40,
                bias_or_weight=0
            )
        ]


name = '8-5封锁战况(削弱前)'
effect = '敌方舰队旗舰存活时，为所有非旗舰单位提供30%减伤；航母、轻母火力-40。'
skill = [NormalMap_080501_1, NormalMap_080501_2]
