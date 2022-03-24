# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 宾夕法尼亚-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *

"""主炮支援(3级)：队伍内每有一个大型船单位都会提升宾夕法尼亚的炮击战4%的伤害。
宾夕法尼亚击中非满血敌方单位时造成额外15%的伤害。
"""


class Skill_104601_1(Skill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.04,
            )
        ]

    def activate(self, friend, enemy):
        buff = self.buff[:]

        target_large = TypeTarget(
            side=1,
            shiptype=LargeShip
        ).get_target(friend, enemy)
        buff_0 = buff[0]
        buff_0.value *= len(target_large)
        self.master.add_buff(buff_0)


class ConditionFinalDamage(FinalDamageBuff):
    """备用接口，随时切换"""
    def __init__(self, timer, name, phase, value_0, value_1,
                 value=0, bias_or_weight=2, atk_request=None, rate=1):
        super().__init__(timer, name, phase, value, bias_or_weight, atk_request, rate)
        self.value_0 = value_0
        self.value_1 = value_1

    def is_active(self, *args, **kwargs):
        try:
            atk = kwargs['atk']
        except:
            atk = args[0]

        if bool(self.atk_request[0](self.timer, atk)):
            self.value = self.value_0 + self.value_1
        else:
            self.value = self.value_0

        return isinstance(self.timer.phase, self.phase) and \
               self.rate_verify()


class Skill_104601_2(Skill):
    """宾夕法尼亚击中非满血敌方单位时造成额外15%的伤害。"""

    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.request = [Request_1]
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.15,
                atk_request=[Request_1]
            )
        ]


class Request_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.status['standard_health'] > \
               self.atk.target.status['health']


skill = [Skill_104601_1, Skill_104601_2]
