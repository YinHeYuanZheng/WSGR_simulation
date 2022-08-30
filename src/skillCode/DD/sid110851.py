# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 黑背豺

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战阶段时，50%概率代替自己上方船只承受攻击，并免疫此次伤害。
（该技能每次战斗只触发一次，大破状态不能发动）"""


class Skill_110851(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            TankBuff(
                timer=timer,
                phase=ShellingPhase,
                target=LocTarget(side=1, loc=[master.loc - 1]),
                value=-1,
                rate=0.5
            )
        ]


name = '拦截护航'
skill = [Skill_110851]
