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
                name='fire',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=6,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target_craft = TypeTarget(
            side=1,
            shiptype=(CL, BC, CA, CAV, CLT)
        ).get_target(friend, enemy)
        num_craft = len(target_craft)

        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            tmp_buff.value *= num_craft
            self.master.add_buff(tmp_buff)


name = '协同作战'
skill = [Skill_111321]
