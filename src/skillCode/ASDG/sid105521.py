# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 絮弗伦-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from AADG_common import *

"""全队索敌值增加7点,对空值增加30点。
索敌成功时,根据装母、航母、要塞、机场、港口、旗舰、轻母的舰种优先级顺序选择其中一艘敌方舰船全阶段无法行动。
自身装备的发射器会视为反潜装备,其索敌值视为对潜值。"""


class Skill_105521_1(PrepSkill):
    """全队索敌值增加7点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=7,
                bias_or_weight=0,
            ),
        ]


class Skill_105521_2(Skill):
    """全队对空值增加30点"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=30,
                bias_or_weight=0,
            ),
        ]


class Skill_105521_3(Skill):
    """索敌成功时,根据装母、航母、要塞、机场、港口、旗舰、轻母的舰种优先级顺序
    选择其中一艘敌方舰船全阶段无法行动。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SkillTarget(
            side=0,
            shiptype=[AV, CV, Fortness, Airfield, Port, Elite, CVL]
        )
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='not_act_phase',
                phase=AllPhase
            )
        ]

    def is_active(self, friend, enemy):
        return self.master.get_recon_flag()


class SkillTarget(TypeTarget):
    """根据装母、航母、要塞、机场、港口、旗舰、轻母的舰种优先级顺序选择其中一艘敌方舰船"""
    def get_target(self, friend, enemy):
        fleet = self.get_target_fleet(friend, enemy)
        type_list = list(self.shiptype)
        for shiptype in type_list:
            target = [ship for ship in fleet if isinstance(ship, shiptype)]
            if len(target):
                return np.random.choice(target, size=1)
        else:
            return []


name = '三坐标定位'
skill = [Skill_105521_1, Skill_105521_2, Skill_105521_3, AADGCommonSkill]
