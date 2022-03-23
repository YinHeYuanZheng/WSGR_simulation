# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 印第安纳-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

"""战列舰支队(3级)：队伍中每有一艘战列舰给印第安纳自身增加火力值3点，命中值4点，
如果队伍中战列舰平均航速大于等于27,增加火力值为4点。
"""


class Skill_103811(Skill):
    def activate(self, friend, enemy):
        # 获取BB
        target_bb = TypeTarget(
            side=1,
            shiptype=BB
        ).get_target(friend, enemy)
        bb_num = len(target_bb)

        # bb均速
        bb_speed = 0
        for tmp_ship in target_bb:
            bb_speed += tmp_ship.get_final_status('speed')
        bb_speed /= bb_num
        if bb_speed >= 27:
            fire_value = 4
        else:
            fire_value = 3

        self.master.add_buff(
            StatusBuff(
                timer=self.timer,
                name='fire',
                phase=AllPhase,
                value=fire_value * bb_num,
                bias_or_weight=0
            )
        )
        self.master.add_buff(
            StatusBuff(
                timer=self.timer,
                name='accuracy',
                phase=AllPhase,
                value=4 * bb_num,
                bias_or_weight=0
            )
        )


skill = [Skill_103811]
