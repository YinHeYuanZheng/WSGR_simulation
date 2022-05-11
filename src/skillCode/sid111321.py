# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 加古-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_111321(Skill):
    """协同作战(3级)：队伍中每一艘巡洋舰（包括自己），都为自己提供火力值加成6点，鱼雷值加成6点。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name="fire",
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name="torpedo",
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        buff = copy.copy(self.buff)

        target_craft = TypeTarget(
            side=1,
            shiptype=(CL, BC, CA, CAV, CLT)
        ).get_target(friend, enemy)

        num_craft = len(target_craft)

        buff[0].value *= num_craft
        buff[1].value *= num_craft
        self.master.add_buff(buff)


skill = [Skill_111321]
