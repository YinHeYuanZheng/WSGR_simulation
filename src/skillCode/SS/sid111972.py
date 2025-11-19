# -*- coding:utf-8 -*-
# Author:huan_yp
# env:py38
# U-47改-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""狼群战术:队伍中每有一艘潜艇，都会增加所有潜艇的命中率 2% 及暴击率 2%，这个技能只在旗舰是 U 型潜艇时生效。"""


class Skill_111972_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=SS)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.02,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.02,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        leader_ship = self.master.master.ship[0]
        if leader_ship.loc != 1:
            raise ValueError('Loc of the first ship in fleet is not 1!')
        return leader_ship.status['tag'] == 'u-ship'

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        count = len(target)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= count
                tmp_target.add_buff(tmp_buff)


name = '狼群战术'
skill = [Skill_111972_1]
