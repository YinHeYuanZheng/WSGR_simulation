# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 鲁莽-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""炮击战阶段自身护甲穿透增加50%，攻击威力不会因耐久损伤而降低，并根据战斗受损程度提高最多30%的攻击威力。
旗舰为E国舰船时，全队E国舰船反航战和T劣势时攻击威力不会受到航向的影响；
如果旗舰为狮级战列舰，则全队每有1艘狮级战利舰，增加全队舰船10%暴击伤害和命中率。"""


class Skill_106231_1(Skill):
    """炮击战阶段自身护甲穿透增加50%，攻击威力不会因耐久损伤而降低，并根据战斗受损程度提高最多30%的攻击威力。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='pierce_coef',
                phase=ShellingPhase,
                value=0.5,
                bias_or_weight=0
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=ShellingPhase
            ),
            HealthBasedBuff(
                timer=timer,
                name='power_buff',
                phase=ShellingPhase,
                value=0.3,
                bias_or_weight=2
            )
        ]


class HealthBasedBuff(CoeffBuff):
    def change_value(self, *args, **kwargs):
        total_health = self.master.status['standard_health']
        health = self.master.status['health']
        self.value = 0.3 * \
                     (total_health - health) / \
                     (total_health - 1)


class Skill_106231_2(Skill):
    """旗舰为E国舰船时，全队E国舰船反航战和T劣势时攻击威力不会受到航向的影响"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = CountryTarget(side=1, country='E')
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_dir_coef',
                phase=AllPhase,
            )
        ]

    def is_active(self, friend, enemy):
        leader = friend.ship[0]
        return leader.status['country'] == 'E' and \
               self.master.get_dir_flag() in [3, 4]


class Skill_106231_3(Skill):
    """如果旗舰为狮级战列舰，则全队每有1艘狮级战利舰，增加全队舰船10%暴击伤害和命中率。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            CoeffBuff(
                timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer,
                name='hit_rate',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
        ]

    def is_active(self, friend, enemy):
        leader = friend.ship[0]
        return leader.status['tag'] == 'lion'

    def activate(self, friend, enemy):
        lion_class = TagTarget(side=1, tag='lion').get_target(friend, enemy)
        num_lion = len(lion_class)

        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= num_lion
                tmp_target.add_buff(tmp_buff)


name = '无畏骑枪'
skill = [Skill_106231_1, Skill_106231_2, Skill_106231_3]
