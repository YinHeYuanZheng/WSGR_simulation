# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 皇家方舟(av)-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""自身火力值增加15点，暴击伤害提高15%，射程增加2档，
队伍中每有1艘E国航母、装母、轻母都会增加自身15%舰载机威力。
自身炮击战阶段对敌方造成两倍伤害。"""


class Skill_104551_1(CommonSkill):
    """自身火力值增加15点。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            )
        ]


class Skill_104551_2(Skill):
    """暴击伤害提高15%，射程增加2档，
    队伍中每有1艘E国航母、装母、轻母都会增加自身15%舰载机威力。
    自身炮击战阶段对敌方造成两倍伤害。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='crit_coef',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='range_buff',
                phase=AllPhase,
                value=2,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=1,
            ),
            CoeffBuff(
                timer=timer,
                name='air_atk_buff',
                phase=AllPhase,
                value=0.15,
                bias_or_weight=2
            ),
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:3]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_target.add_buff(tmp_buff)

        e_cv = CombinedTarget(
            side=1,
            target_list=[
                CountryTarget(side=1, country='E'),
                TypeTarget(side=1, shiptype=(AV, CV, CVL))
            ]
        ).get_target(friend, enemy)
        for tmp_target in target:
            buff_0 = copy.copy(self.buff[3])
            buff_0.value *= len(e_cv)
            tmp_target.add_buff(buff_0)


name = '新时代'
skill = [Skill_104551_1, Skill_104551_2]
