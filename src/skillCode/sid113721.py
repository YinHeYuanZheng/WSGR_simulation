# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 早春

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""突入作战(3级)：增加队伍中航母、装母、轻母9点对空值。
先制鱼雷、鱼雷战阶段提升自身和队伍里所有驱逐、潜艇、雷巡15%的伤害，队伍中每有一个驱逐、潜艇、雷巡单位都会给该伤害增加3%。
"""


class Skill_113721_1(Skill):
    """增加队伍中航母、装母、轻母9点对空值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(CV, CVL, AV))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=9,
                bias_or_weight=0
            )
        ]


class Skill_113721_2(Skill):
    """先制鱼雷、鱼雷战阶段提升自身和队伍里所有驱逐、潜艇、雷巡15%的伤害，队伍中每有一个驱逐、潜艇、雷巡单位都会给该伤害增加3%"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(DD, SS, CLT))
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=TorpedoPhase,
                value=0.15
            )
        ]

    def activate(self, friend, enemy):
        # 队伍中每有一个驱逐、潜艇、雷巡单位都会给该伤害增加3%"
        buff = copy.copy(self.buff[0])
        target_needed = TypeTarget(side=1, shiptype=(
            DD, SS, CLT)).get_target(friend, enemy)  # 获取驱逐
        buff.value = buff.value + target_needed.count * 0.03
        self.master.add_buff(buff)


name = '突入作战'
skill = [Skill_113721_1, Skill_113721_2]
