# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 圣乔治-2

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""巨炮火力(3级)：队伍内战列数量大于等于2时，提升自身12点装甲值，并额外提升自身炮击战20%的伤害；
队伍内战巡数量大于等于2时，提升自身20%的暴击率和15点命中值。
命中比自身火力低的单位时，对其造成15%额外伤害
"""


class Skill_113802_1(Skill):
    """队伍内战列数量大于等于2时，提升自身12点装甲值，并额外提升自身炮击战20%的伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='armor',
                phase=(AllPhase,),
                value=12,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=(ShellingPhase,),
                value=0.2
            )
        ]

    def is_active(self, friend, enemy):
        target = TypeTarget(
            side=1,
            shiptype=BB
        ).get_target(friend, enemy)
        num = len(target)
        return num >= 2


class Skill_113802_2(Skill):
    """队伍内战巡数量大于等于2时，提升自身20%的暴击率和15点命中值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=(AllPhase,),
                value=0.2,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=(AllPhase,),
                value=15,
                bias_or_weight=0
            )
        ]

    def is_active(self, friend, enemy):
        target = TypeTarget(
            side=1,
            shiptype=BC
        ).get_target(friend, enemy)
        num = len(target)
        return num >= 2


class Skill_113802_3(Skill):
    """命中比自身火力低的单位时，对其造成15%额外伤害"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.15,
                atk_request=[ATKRequest_1]
            )
        ]


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return self.atk.target.get_final_status("fire") < \
               self.atk.atk_body.get_final_status("fire")


skill = [Skill_113802_1, Skill_113802_2, Skill_113802_3]
