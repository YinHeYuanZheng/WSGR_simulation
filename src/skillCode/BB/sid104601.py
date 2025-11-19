# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 宾夕法尼亚-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

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
        buff_0 = copy.copy(self.buff[0])
        target_large = TypeTarget(side=1, shiptype=LargeShip).get_target(friend, enemy)  # 获取大型船
        buff_0.value *= len(target_large)
        self.master.add_buff(buff_0)


class Skill_104601_2(Skill):
    """宾夕法尼亚击中非满血敌方单位时造成额外15%的伤害。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
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
