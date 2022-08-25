# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 欧根亲王改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身5点幸运值，自身50%的幸运值视为装甲值。
自身非大破状态时，炮击战阶段代替相邻水上舰船承受攻击，并免疫这次伤害(每次只对一艘舰船生效，每场战斗只生效2次)。"""


class Skill_110381_1(CommonSkill):
    """增加自身5点幸运值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='luck',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
        ]


class Skill_110381_2(Skill):
    """自身50%的幸运值视为装甲值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=.5,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        luck = self.master.get_final_status('luck')
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= luck
                tmp_target.add_buff(tmp_buff)


class Skill_110381_3(Skill):
    """自身非大破状态时，炮击战阶段代替相邻水上舰船承受攻击，并免疫这次伤害(每次只对一艘舰船生效，每场战斗只生效2次)。"""
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
                value=-1,
                rate=1,
                exhaust=2,
            )
        ]


name = '战线防御'
skill = [Skill_110381_1, Skill_110381_2, Skill_110381_3]
