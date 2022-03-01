# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 萨拉托加改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110231(Skill):
    """队伍中每1艘自身以外的航母、装母、轻母，都会提高自身7%的舰载机威力。
    如果是E国额外提高7%"""

    def activate(self, friend, enemy):
        # 获取航系
        target_craft = TypeTarget(
            side=1,
            shiptype=(CV, AV, CVL)
        ).get_target(friend, enemy)

        # 去掉自身
        target_craft.remove(self.master)

        # 获取E国航系
        target_e_craft = [ship for ship in target_craft
                          if ship.status['country'] == 'E']

        num_craft = len(target_craft)
        num_e_craft = len(target_e_craft)
        buff_value = 0.07 * (num_craft + num_e_craft)

        self.master.add_buff(
            CoeffBuff(
                timer=self.timer,
                name='air_atk_buff',
                phase=(AllPhase,),
                value=buff_value,
                bias_or_weight=2)
        )


skill = [Skill_110231]
