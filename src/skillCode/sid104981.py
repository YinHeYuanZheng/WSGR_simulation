# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 复仇-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""	队伍中每有一艘埃塞克斯级航空母舰都会增加自身8%的舰载机威力。"""


class Skill_104981(Skill):

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.buff = [
            CoeffBuff(
                timer=self.timer,
                name='air_atk_buff',
                phase=(AllPhase,),
                value=0.08,
                bias_or_weight=2
            )
        ]

    def activate(self, friend, enemy):
        buff = self.buff[:]

        # 获取埃塞克斯级
        target_essex = TagTarget(
            side=1,
            tag='essex'
        ).get_target(friend, enemy)

        buff_0 = buff[0]
        buff_0.value *= len(target_essex)
        self.master.add_buff(buff_0)


skill = [Skill_104981]
