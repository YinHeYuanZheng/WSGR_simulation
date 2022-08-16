# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 欧根亲王改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""战斗中，全队总幸运每10点增加自身装甲值1点，每10点增加自身火力值1点。"""


class Skill_110382(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=1,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=1,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        luck = 0
        for tmp_ship in friend.ship:
            luck += tmp_ship.get_final_status('luck')
        luck_mul = luck // 10

        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= luck_mul
                tmp_target.add_buff(tmp_buff)


name = '不死鸟'
skill = [Skill_110382]
