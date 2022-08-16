# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 黄蜂改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战中，自身在受到伤害后对敌人发动反击，必然命中，伤害为普通攻击的100%。（每场战斗限1次，大破无法发动）"""


class Skill_112251(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            HitBack(
                timer=timer,
                phase=ShellingPhase,
            )
        ]


name = '狂蜂'
skill = [Skill_112251]
