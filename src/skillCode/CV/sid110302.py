# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 萨拉托加改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


class Skill_110302(Skill):
    """队伍中每1艘自身以外的航母、装母、轻母，都会提高自身7%的舰载机威力。
    如果是E国额外提高7%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.07,
                bias_or_weight=2
            )
        ]

    def activate(self, friend, enemy):
        buff = copy.copy(self.buff[0])

        target_craft = TypeTarget(side=1, shiptype=(CV, AV, CVL)
                                  ).get_target(friend, enemy)  # 获取航系
        if self.master in target_craft:
            target_craft.remove(self.master)                   # 去掉自身
        target_e_craft = [ship for ship in target_craft
                          if ship.status['country'] == 'E']    # 获取E国航系
        if self.master in target_e_craft:
            target_e_craft.remove(self.master)                 # 去掉自身

        num_craft = len(target_craft)
        num_e_craft = len(target_e_craft)

        buff.value *= (num_craft + num_e_craft)
        self.master.add_buff(buff)


name = '罗宾'
skill = [Skill_110302]
