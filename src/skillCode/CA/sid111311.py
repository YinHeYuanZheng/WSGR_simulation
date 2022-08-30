# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 古鹰-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战阶段时，60%概率代替旗舰承受攻击，并获得80%伤害减免（该技能大破状态不能发动，自身旗舰无效）。"""


class Skill_111311(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            TankBuff(
                timer=timer,
                phase=ShellingPhase,
                target=LocTarget(side=1, loc=[1]),
                value=-0.8,
                rate=0.6,
                exhaust=None
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.loc != 1


name = '战线援护'
skill = [Skill_111311]
