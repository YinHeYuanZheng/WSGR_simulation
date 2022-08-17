# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 欧根亲王改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战阶段时，50%概率代替相邻水上舰船承受攻击，并获得80%伤害减免（每场战斗仅触发一次，且该技能大破状态不能发动）。"""


class Skill_110381(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            TankBuff(
                timer=timer,
                phase=ShellingPhase,
                target=CombinedTarget(
                    side=1,
                    target_list=[
                        NearestLocTarget(
                            side=1,
                            master=master,
                            radius=1,
                            direction='near'
                        ),
                        AntiTypeTarget(
                            side=1,
                            shiptype=Submarine
                        )
                    ],
                ),
                value=-0.8,
                rate=0.5
            )
        ]


name = '战线防御'
skill = [Skill_110381]
