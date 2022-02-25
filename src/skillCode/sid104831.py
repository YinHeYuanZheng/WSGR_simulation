# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 胜利-1

from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *

"""自身对战列舰、战列巡洋舰造成的伤害提高10%/20%/30%。
自身与相邻上方舰船舰载机威力提高5%/10%/15%，
如果相邻上方为E国或U国舰船，则其舰载机威力额外提高4%/7%/10%。"""


class Skill_104831_1(Skill):
    """自身对战列舰、战列巡洋舰造成的伤害提高10%/20%/30%。"""

    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                name='final_damage_buff',
                phase=(AllPhase,),
                value=0.3,
                atk_request=[BuffRequest_1],
            )
        ]

    def is_active(self, friend, enemy):
        return True


class Skill_104831_2(Skill):
    """自身与相邻上方舰船舰载机威力提高5%/10%/15%，"""

    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='up',
            master_include=True,
            shiptype=(CV, CVL, AV)
        )
        self.buff = [
            CoeffBuff(
                name='air_atk_buff',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=2
            )
        ]


class Skill_104831_3(Skill):
    """如果相邻上方为E国或U国舰船，则其舰载机威力额外提高4%/7%/10%。"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='up',
            shiptype=(CV, CVL, AV)
        )
        self.buff = [
            CoeffBuff(
                name='air_atk_buff',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=2
            )
        ]

    def is_active(self, friend, enemy):
        return bool(self.request[0](self.master, friend, enemy))


class Request_1(Request):
    def __bool__(self):
        target = NearestLocTarget(
            side=1,
            master=self.master,
            radius=1,
            direction='up',
            shiptype=(CV, CVL, AV)
        )
        country = target.get_target(self.friend, self.enemy).get_status(name='country')
        return country == 'E' or country == 'U'


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (BB, BC))


skill = [Skill_104831_1, Skill_104831_2, Skill_104831_3]
