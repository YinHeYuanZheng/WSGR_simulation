# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 五十铃改-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""装备的防空炮将同时视为对潜装备，并且防空炮的对空值的80%视为对潜值。
装备的对潜装备同时视为防空炮，并且对潜装备的对潜值的80%视为对空值。"""


class Skill_110451_1(CommonSkill):
    def activate(self, friend, enemy):
        new_equip_list = []
        for tmp_equip in self.master.equipment:
            if isinstance(tmp_equip, AntiAirGun):
                # 重新创建合并类装备
                new_equip = CombineEquipment(
                    self.timer,
                    tmp_equip.master,
                    tmp_equip.enum
                )
                # 复制所有属性
                new_equip.copy_equip(tmp_equip)
                # 防空炮的对空值的80%视为对潜值
                antiair = tmp_equip.status.get('antiair', 0)
                new_equip.set_status('antisub', 0.8 * antiair)
                new_equip_list.append(new_equip)
            elif isinstance(tmp_equip, DepthMine):
                # 重新创建合并类装备
                new_equip = CombineEquipment(
                    self.timer,
                    tmp_equip.master,
                    tmp_equip.enum
                )
                # 复制所有属性
                new_equip.copy_equip(tmp_equip)
                # 对潜装备的对潜值的80%视为对空值
                new_equip.set_status('antiair', 0.8 * tmp_equip.status['antisub'])
                new_equip_list.append(new_equip)
            else:
                new_equip_list.append(tmp_equip)
        self.master.set_equipment(new_equip_list)


class CombineEquipment(DepthMine, AntiAirGun):
    def copy_equip(self, equipment):
        if not isinstance(equipment, (DepthMine, AntiAirGun)):
            raise TypeError(f"Wrong type {type(equipment)} to copy")

        # 复制属性
        self.status = equipment.status
        # 复制技能
        e_skill, _ = equipment.get_skill()
        self.add_skill(e_skill)
        # 复制加成
        self.common_buff = equipment.common_buff
        self.temper_buff = equipment.temper_buff


name = '空潜一体'
skill = [Skill_110451_1]
