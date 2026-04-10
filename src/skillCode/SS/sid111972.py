# -*- coding:utf-8 -*-
# Author:huan_yp
# Edited by: 银河远征(20260410)
# env:py38
# U-47改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""狼群战术：队伍中每有一艘潜艇，全队潜艇的命中率、暴击率与伤害提升3%；
若旗舰为U型潜艇，队伍中的U型潜艇再额外获得1倍效果。"""


class Skill_111972_1(Skill):
    """队伍中每有一艘潜艇，全队潜艇的命中率、暴击率与伤害提升3%"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=SS)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.03,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.03,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.03
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        ss_count = len(target)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= ss_count
                tmp_target.add_buff(tmp_buff)


class Skill_111972_2(Skill):
    """若旗舰为U型潜艇，队伍中的U型潜艇再额外获得1倍效果"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TagTarget(side=1, tag='u-ship')
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.03,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.03,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.03
            )
        ]

    def is_active(self, friend, enemy):
        leader_ship = self.master.master.ship[0]
        if leader_ship.loc != 1:
            raise ValueError('Loc of the first ship in fleet is not 1!')
        return leader_ship.status['tag'] == 'u-ship'

    def activate(self, friend, enemy):
        ss_count = len(TypeTarget(side=1, shiptype=SS).get_target(friend, enemy))
        if ss_count == 0:
            return
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= ss_count
                tmp_target.add_buff(tmp_buff)


name = '狼群战术'
skill = [Skill_111972_1, Skill_111972_2]
