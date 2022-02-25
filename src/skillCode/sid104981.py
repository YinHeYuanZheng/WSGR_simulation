# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 复仇-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
"""	队伍中每有一艘埃塞克斯级航空母舰都会增加自身8%的舰载机威力。"""


class Skill_104981(Skill):
    def activate(self, friend, enemy):
        # todo 获取饺子型
        target_craft = TagTarget(
            side=1,
            value='essex'
        ).get_target(friend, enemy)

        value = 0.08 * len(TagTarget)
        self.master.add_buff(
            CoeffBuff(
                name='air_atk_buff',
                phase=(AllPhase,),
                value=value,
                bias_or_weight=2,
            )
        )


class Request_1(Request):
    def __bool__(self):
        pass


skill = [Skill_104981]
