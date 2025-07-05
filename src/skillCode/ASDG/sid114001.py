# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 七省联盟改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""根据队伍国籍种类数量每有一种增加全队3点回避值和提高3%暴击率。
自身和相邻舰船射程增加1档。
炮击战阶段自身有50%概率同时攻击2个目标。"""


class Skill_114001_1(Skill):
    """根据队伍国籍种类数量每有一种增加全队3点回避值和提高3%暴击率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.03,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        # 获取队伍国籍种类数量
        country = [ship.status['country'] for ship in friend.ship]
        country_num = len(set(country))

        # 根据国籍种类数量增加全队回避值和暴击率
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= country_num
                tmp_target.add_buff(tmp_buff)


class Skill_114001_2(Skill):
    """自身和相邻舰船射程增加1档。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='near',
            master_include=True
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range_buff',
                phase=AllPhase,
                value=1,
                bias_or_weight=0
            )
        ]


class Skill_114001_3(Skill):
    """炮击战阶段自身有50%概率同时攻击2个目标。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            MultipleAtkBuff(
                timer=timer,
                name='multi_attack',
                phase=ShellingPhase,
                num=2,
                rate=0.5
            )
        ]


name = '联合突击'
skill = [Skill_114001_1, Skill_114001_2, Skill_114001_3]
