# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 金刚-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""高速战舰(3级)：编队内J国重巡，战列，战巡，航战，航巡的火力+8，命中+8。
"""


class Skill_110141(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeStatusTarget(side=1,
                                       shiptype=(CA, BB, BC, BBV, CAV))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            )
        ]


class TypeStatusTarget(TypeTarget):
    def get_target(self, friend, enemy):
        fleet = self.get_target_fleet(friend, enemy)
        target = []
        for ship in fleet:
            if isinstance(ship, self.shiptype) and ship.status['country'] == 'J':
                target.append(ship)
        return target


name = '高速战舰'
skill = [Skill_110141]
