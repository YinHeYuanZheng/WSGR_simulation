# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 絮弗伦-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.equipment import *

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
        if isinstance(enemy, Fleet):
            enemy = enemy.ship
        fleet = enemy

        type_list = list(self.shiptype)
        for shiptype in type_list:
            target = [ship for ship in fleet if isinstance(ship, shiptype)]
            if len(target):
                return np.random.choice(target, size=1)
        else:
            return []


class Skill_105521_4(CommonSkill):
    """自身装备的发射器会视为反潜装备，其索敌值视为反潜值"""
    def activate(self, friend, enemy):
        new_equip_list = []
        for tmp_equip in self.master.equipment:
            if isinstance(tmp_equip, Launcher):
                # 重新创建合并类装备
                new_equip = CombineEquipment(
                    self.timer,
                    tmp_equip.master,
                    tmp_equip.enum
                )
                # 复制所有属性
                new_equip.copy_equip(tmp_equip)
                # 发射器的索敌值视为对潜值
                new_equip.set_status('antisub', tmp_equip.status['recon'])
                new_equip_list.append(new_equip)
            else:
                new_equip_list.append(tmp_equip)
        self.master.set_equipment(new_equip_list)


class CombineEquipment(DepthMine, Launcher):
    def copy_equip(self, equipment):
        if not isinstance(equipment, Launcher):
            raise TypeError(f"Wrong type {type(equipment)} to copy")

        # 复制属性
        self.status = equipment.status
        # 复制技能
        e_skill, _ = equipment.get_skill()
        self.add_skill(e_skill)
        # 复制加成
        self.common_buff = equipment.common_buff
        self.temper_buff = equipment.temper_buff


name = '三坐标定位'
skill = [Skill_105521_1, Skill_105521_2, Skill_105521_3, Skill_105521_4]
