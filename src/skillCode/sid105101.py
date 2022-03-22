# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# G14-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""海平面突袭：队伍中每有1艘J国舰船都会增加自身6%的舰载机威力。
首轮炮击战阶段40%概率同时攻击两个目标且必定命中，队伍中每有1艘装甲航母都会增加15%发动概率"""


class Skill_105101_1(Skill):
    def activate(self, friend, enemy):
        # 队伍中每有1艘J国舰船都会增加自身6%的舰载机威力
        # 获取J国
        target_j = TagTarget(
            side=1,
            tag='J',
            tag_name='country'
        ).get_target(friend, enemy)

        buff_value = 0.06 * len(target_j)
        self.master.add_buff(
            CoeffBuff(
                timer=self.timer,
                name='air_atk_buff',
                phase=(AllPhase,),
                value=buff_value,
                bias_or_weight=2
            )
        )

        # 首轮炮击战阶段40%概率同时攻击两个目标且必定命中，队伍中每有1艘装甲航母都会增加15%发动概率
        # 获取装母
        target_av = TypeTarget(
            side=1,
            shiptype=AV
        ).get_target(friend, enemy)
        rate_value = min(1., 0.4 + 0.15 * len(target_av))
        self.master.add_buff(
            MultipleAtkBuff(
                timer=self.timer,
                name='multi_attack',
                phase=FirstShellingPhase,
                num=2,
                rate=rate_value,
                coef={'must_hit': True}
            )
        )


skill = [Skill_105101_1]
