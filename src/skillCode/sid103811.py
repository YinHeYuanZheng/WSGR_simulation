# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 印第安纳-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""战列舰支队(3级)：队伍中每有一艘战列舰给印第安纳自身增加火力值3点，命中值4点，
如果队伍中战列舰平均航速大于等于27,增加火力值为4点。
"""


class Skill_103811(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.buff = [
            StatusBuff(
                timer=self.timer,
                name='fire',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=self.timer,
                name='accuracy',
                phase=AllPhase,
                value=4,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        buff = self.buff[:]

        # 火力buff
        buff_0 = buff[0]
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
            buff_0.value = 4
        else:
            buff_0.value = 3

        buff_0.value *= bb_num
        self.master.add_buff(buff_0)

        # 命中buff
        buff_1 = buff[1]
        buff_1.value *= bb_num
        self.master.add_buff(buff_1)


skill = [Skill_103811]
