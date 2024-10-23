# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# V方案-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""根据队伍国籍种类数量（I国以外）每有一种增加全队5点火力值和装甲值。"""


class Skill_102011_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        # 获取队伍中非I国的国籍种类数量
        country = [ship.status['country'] for ship in friend.ship
                   if ship.status['country'] != 'I']
        country_num = len(set(country))

        # 根据国籍种类数量增加全队火力值和装甲值
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= country_num
                tmp_target.add_buff(tmp_buff)


name = '亚得里亚之梦'
skill = [Skill_102011_1]
