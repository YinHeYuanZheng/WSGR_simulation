# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 巴尔的摩改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""不朽的英魂(3级)：当自身在场时，队伍中每有一艘U国重巡洋舰，则为全队轻巡、重巡、航巡提供5火力加成，
队伍中每有一艘U国轻巡洋舰，则为全队轻巡、重巡、航巡提供5对空和回避加成。"""


class U_TypeTarget(TypeTarget):
    def get_target(self, friend, enemy):
        fleet = self.get_target_fleet(friend, enemy)
        target = [ship for ship in fleet
                  if isinstance(ship, self.shiptype) and ship.status['country'] == 'U']
        return target


class Skill_112411_1(Skill):
    """队伍中每有一艘U国重巡洋舰，则为全队轻巡、重巡、航巡提供5火力加成"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(CL, CA, CAV))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        u_ca = U_TypeTarget(side=1, shiptype=CA).get_target(friend, enemy)
        if len(u_ca) == 0:
            return
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= len(u_ca)
                tmp_target.add_buff(tmp_buff)


class Skill_112411_2(Skill):
    """队伍中每有一艘U国轻巡洋舰，则为全队轻巡、重巡、航巡提供5对空和回避加成"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(CL, CA, CAV))
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        u_cl = U_TypeTarget(side=1, shiptype=CL).get_target(friend, enemy)
        if len(u_cl) == 0:
            return
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value *= len(u_cl)
                tmp_target.add_buff(tmp_buff)


name = '不朽的英魂'
skill = [Skill_112411_1, Skill_112411_2]
