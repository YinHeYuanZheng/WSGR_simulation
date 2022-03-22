# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 宾夕法尼亚-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *
from src.wsgr.formulas import *
"""主炮支援(3级)：队伍内每有一个大型船单位都会提升宾夕法尼亚的炮击战4%的伤害。
宾夕法尼亚击中非满血敌方单位时造成额外15%的伤害。
"""


class Skill_104601_1(Skill):
    """队伍内每有一个大型船单位都会提升宾夕法尼亚的炮击战4%的伤害。"""

    def activate(self, friend, enemy):
        largeShip = TypeTarget(side=1,shiptype=LargeShip).get_target(friend, enemy)
        SkillNumber = len(largeShip) * 0.04
        self.master.add_buff(
            FinalDamageBuff(
                self.timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=SkillNumber
            )
        )


class Skill_104601_2(Skill):
    """宾夕法尼亚击中非满血敌方单位时造成额外15%的伤害。"""

    def __init__(self, master, timer):
        super().__init__(master, timer)
        self.target = SelfTarget(master)
        self.request = [Request_1]
        self.buff = [
            FinalDamageBuff(
                self.timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.15,
                atk_request=[Request_1]
            )
        ]


class Request_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.status['total_health'] > self.atk.target.status['health']


skill = [Skill_104601_1, Skill_104601_2]
