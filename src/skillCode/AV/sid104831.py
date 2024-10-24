# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 胜利-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身对战列舰、战列巡洋舰造成的伤害提高30%。
自身与相邻上方舰船舰载机威力提高15%，
如果相邻上方为E国或U国舰船，则其舰载机威力额外提高10%。"""


class Skill_104831_1(Skill):
    """自身对战列舰、战列巡洋舰造成的伤害提高30%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.3,
                atk_request=[BuffRequest_1]
            )
        ]


class BuffRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, (BB, BC))


class Skill_104831_2(Skill):
    """自身与相邻上方舰船舰载机威力提高15%，"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='up',
            master_include=True,
        )
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=2
            )
        ]


class Skill_104831_3(Skill):
    """如果相邻上方为E国或U国舰船，则其舰载机威力额外提高10%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = NearestLocTarget(
            side=1,
            master=master,
            radius=1,
            direction='up',
        )
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=2
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            if tmp_target.status['country'] in 'UE':
                for tmp_buff in self.buff[:]:
                    tmp_buff = copy.copy(tmp_buff)
                    tmp_target.add_buff(tmp_buff)


name = '协同出击'
skill = [Skill_104831_1, Skill_104831_2, Skill_104831_3]
