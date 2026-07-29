# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 8-4封锁战况(削弱后)

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_080402_1(PrepSkill):
    """敌方舰队每存活一个非旗舰单位都会为旗舰提供5%减伤"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = LocTarget(side=0, loc=[1])
        self.buff = [
            EnemySurviveBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-0.05
            )
        ]


class EnemySurviveBuff(FinalDamageBuff):
    def change_value(self, *args, **kwargs):
        alive_num = 0
        for tmp_ship in self.master.master.ship:
            if tmp_ship.loc != 1 and tmp_ship.damaged <= 3:
                alive_num += 1
        self.value = -0.05 * alive_num


name = '8-4封锁战况(削弱后)'
effect = '敌方舰队每存活一个非旗舰单位都会为旗舰提供5%减伤。'
skill = [NormalMap_080402_1]
