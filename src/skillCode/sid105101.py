# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# G14-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

"""海平面突袭：队伍中每有1艘J国舰船都会增加自身6%的舰载机威力。
首轮炮击战阶段40%概率同时攻击两个目标且必定命中，队伍中每有1艘装甲航母都会增加15%发动概率"""


class Skill_105101_1(Skill):
    """队伍中每有1艘J国舰船都会增加自身6%的舰载机威力"""
    def activate(self, friend, enemy):
        # 获取埃塞克斯级
        target_j = TagTarget(
            side=1,
            tag='J',
            tag_name='country'
        ).get_target(friend, enemy)

        buff_value = 0.06 * len(target_j)
        self.master.add_buff(
            CoeffBuff(
                name='air_atk_buff',
                phase=(AllPhase,),
                value=buff_value,
                bias_or_weight=2,
            )
        )


skill = [Skill_105101_1]
