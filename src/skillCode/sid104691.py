# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 本宁顿-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.equipment import *

"""特混空袭(3级)：航空战阶段，自身增加20%伤害，队伍内其他航母类(航母、装母、轻母)单位增加14%伤害；
炮击战阶段，队伍内非航母类单位增加18%伤害。"""


class Skill_104691_1(Skill):
    """航空战阶段，自身增加20%伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=(AirPhase,),
                value=0.2
            )
        ]


class Skill_104691_2(Skill):
    """航空战阶段，队伍内其他航母类(航母、装母、轻母)单位增加14%伤害"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(CV, CVL, AV))
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=(AirPhase,),
                value=0.14
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        target.remove(self.master)  # 去除自身
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_target.add_buff(tmp_buff)


class Skill_104691_3(Skill):
    """炮击战阶段，队伍内非航母类单位增加18%伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = AntiTypeTarget(side=1, shiptype=(CV, CVL, AV))
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=(ShellingPhase,),
                value=0.18
            )
        ]


skill = [Skill_104691_1, Skill_104691_2, Skill_104691_3]
