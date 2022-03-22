# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 印第安纳-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
from src.wsgr.formulas import *

"""战列舰支队(3级)：队伍中每有一艘战列舰给印第安纳自身增加火力值3点，命中值4点，
如果队伍中战列舰平均航速大于等于27,增加火力值为4点。
"""


class Skill_103811(Skill):
    """队伍中每有一艘战列舰给印第安纳自身增加火力值3点，
    命中值4点，如果队伍中战列舰平均航速大于等于27,增加火力值为4点。"""

    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)

    def active(self, friend, enemy):
        target_craft = TypeTarget(
            side=1,
            shiptype=(CV, AV, CVL)
        ).get_target(friend, enemy)
        speed = 0
        BBNumber = len(target_craft)
        for i in range(BBNumber):
            speed += target_craft[i].status['speed']
        avgSpeed = speed / BBNumber
        self.master.add_buff(
            StatusBuff(
                self.timer,
                name='accuracy',
                phase=AllPhase,
                value=4 * BBNumber,
                bias_or_weight=0
            )
        )
        if avgSpeed < 27:
            self.master.add_buff(
                StatusBuff(
                    self.timer,
                    name='fire',
                    phase=AllPhase,
                    value=3 * BBNumber,
                    bias_or_weight=0
                )
            )
        else:
            self.master.add_buff(
                StatusBuff(
                    self.timer,
                    name='fire',
                    phase=AllPhase,
                    value=4 * BBNumber,
                    bias_or_weight=0
                )
            )


skill = [Skill_103811]
