# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# 拉菲

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""技能效果随技能等级提升而增加
Lv.1: 昼战时攻击力不会因为自身受到的HP损伤而降低
Lv.2: 根据所受到损伤提升暴击率
Lv.3: 中破状态下免疫航空攻击"""


class Skill_111831(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
        ]
    
name = '不惧神风'
skill = [Skill_111831]
