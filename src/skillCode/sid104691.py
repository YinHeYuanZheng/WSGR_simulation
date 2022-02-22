# -*- coding:utf-8 -*-
# Author:zzhh225
# env:py38
# 本宁顿-1
from ..wsgr.formulas import AirAtk
from ..wsgr.skill import *
from ..wsgr.ship import *
from ..wsgr.phase import *
from ..wsgr.equipment import *


class Skill_104691_1(Skill):
    """特混空袭(3级)：航空战阶段，自身增加20%伤害，"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = SelfTarget(master)
        self.buff = [
            FinalDamageBuff(
                name='final_damage_buff',
                phase=(AirPhase, ),
                value=0.2,
                bias_or_weight=2,
                atk_request=[ATKRequest_1]
            )
        ]

    def is_active(self, friend, enemy):
        return True


class Skill_104691_2(Skill):
    """队伍内其他航母类(航母、装母、轻母)单位增加14%伤害；"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = TypeTarget(side=1, shiptype=(CV, CVL, AV))
        self.buff = [
            FinalDamageBuff(
                name='final_damage_buff',
                phase=(AirPhase, ),
                value=0.14,
                bias_or_weight=2,
                atk_request=[ATKRequest_1]
            )
        ]

    def is_active(self, friend, enemy):
        return True


class Skill_104691_3(Skill):
    """炮击战阶段，队伍内非航母类单位增加18%伤害。"""
    def __init__(self, master):
        super().__init__(master)
        self.request = [Request_1]
        self.target = AntiTypeTarget(side=1, shiptype=(CV, CVL, AV))
        self.buff = [
            FinalDamageBuff(
                name='final_damage_buff',
                phase=(ShellingPhase, ),
                value=0.18,
                bias_or_weight=2,
                atk_request=[ATKRequest_2]
            )
        ]

    def is_active(self, friend, enemy):
        return True


class AntiTypeTarget(TypeTarget):
    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = [ship for ship in fleet if not isinstance(ship, self.shiptype)]
        return target


class ATKRequest_1(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, AirAtk)


class ATKRequest_2(ATKRequest):
    def __bool__(self):
        return isinstance(self.atk, AirAtk)  # todo 非航系伤害


class Request_1(Request):
    def __bool__(self):
        pass


skill = [Skill_104691_1, Skill_104691_2, Skill_104691_3]
