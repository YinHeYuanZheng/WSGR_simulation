# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 翔鹤改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战阶段时，25%概率代替队伍中其他航母、装母、轻母承受攻击，并获得80%伤害减免
（每场战斗仅触发一次，且该技能大破状态不能发动）。"""


class Skill_112201(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            TankBuff(
                timer=timer,
                phase=ShellingPhase,
                target=TypeTarget(side=1, shiptype=(CV, AV, CVL)),
                value=-0.8,
                rate=0.25,
            )
        ]


name = '被害担当'
skill = [Skill_112201]
