# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 防驱通用技能

from src.wsgr.skill import *
from src.wsgr.ship import *

__all__ = ['AADGCommonSkill']

"""自身装备的发射器会视为反潜装备，其索敌值视为反潜值"""

class AADGCommonSkill(CommonSkill):
    def activate(self, friend, enemy):
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
                recon = tmp_equip.status.get('recon', 0)
                new_equip.set_status('antisub', recon)
                new_equip_list.append(new_equip)
            else:
                new_equip_list.append(tmp_equip)
        self.master.set_equipment(new_equip_list)
