# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 法戈-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""增加自身15点索敌值和40点对空值，自身装备防空炮的对空值视为火力值。"""


class Skill_105221_1(CommonSkill):
    """增加自身15点索敌值和40点对空值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CommonBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=15,
                bias_or_weight=0
            ),
            CommonBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=40,
                bias_or_weight=0
            )
        ]


class Skill_105221_2(CommonSkill):
    """自身装备防空炮的对空值视为火力值"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=(AntiAirGun,))
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=1,
                bias_or_weight=0
            )
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.value = tmp_target.status['antiair']
                tmp_target.add_buff(tmp_buff)


name = '新锐轻巡'
skill = [Skill_105221_1, Skill_105221_2]


