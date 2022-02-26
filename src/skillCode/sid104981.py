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
        # 获取埃塞克斯级
        target_essex = TagTarget(
            side=1,
            tag='essex'
        ).get_target(friend, enemy)

        buff_value = 0.08 * len(target_essex)
        self.master.add_buff(
            CoeffBuff(
                name='air_atk_buff',
                phase=(AllPhase,),
                value=buff_value,
                bias_or_weight=2,
            )
        )


skill = [Skill_104981]
