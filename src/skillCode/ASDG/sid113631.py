# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 炽热-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from AADG_common import *

"""全队航速增加3点。
自身装备的发射器会视为反潜装备，其索敌值视为对潜值。
自身反潜值视为火力值，攻击潜艇时命中率和伤害提高25%。"""


class Skill_113631_1(PrepSkill):
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='speed',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            )
        ]


class Skill_113631_2(Skill):
    """自身反潜值视为火力值，攻击潜艇时命中率和伤害提高25%。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=1,
                bias_or_weight=0
            ),
            AtkBuff(
                timer=timer,
                name='hit_rate',
                phase=AllPhase,
                value=.25,
                bias_or_weight=0,
                atk_request=[ATKRequest_1]
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=.25,
                atk_request=[ATKRequest_1]
            )
        ]

    def activate(self, friend, enemy):
        evasion = self.master.get_final_status('antisub')
        buff0 = copy.copy(self.buff[0])
        buff0.value *= evasion
        self.master.add_buff(buff0)

        for tmp_buff in self.buff[1:]:
            tmp_buff = copy.copy(tmp_buff)
            self.master.add_buff(tmp_buff)


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk.target, SS)


name = '胜利巡游'
skill = [Skill_113631_1, Skill_113631_2, AADGCommonSkill]
