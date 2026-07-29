# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 6/7图战利品战况(削弱后)
from src.skillCode.MapEnv.map070001 import NormalMap_070001_1
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class NormalMap_070002_1(PrepSkill):
    """我方主力舰火力+15"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=MainShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class NormalMap_070002_2(PrepSkill):
    """护卫舰暴击率+10%"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=CoverShip)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            )
        ]


class NormalMap_070002_3(PrepSkill):
    """大型船装甲+15"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=LargeShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class NormalMap_070002_4(PrepSkill):
    """中型船命中+15"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=MidShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class NormalMap_070002_5(PrepSkill):
    """小型船闪避+15"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=SmallShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


name = '6/7图战利品战况(削弱后)'
effect = '我方主力舰火力+15，护卫舰暴击率+10%，大型船装甲+15，中型船命中+15，小型船闪避+15'
skill = [NormalMap_070002_1, NormalMap_070002_2, NormalMap_070002_3,
         NormalMap_070002_4, NormalMap_070002_5]
