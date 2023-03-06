# -*- coding:utf-8 -*-
# Author:stars
# env:py38
# 基阿特

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
from src.wsgr.equipment import *

"""驾束制导(3级)：提高自身携带导弹和发射架类装备10点火力值，
随机降低三名敌方单位15回避值、命中值、火力值和装甲值，对位敌人不参与首轮炮击。
自身装备的发射器会视为反潜装备，其索敌值视为反潜值"""


class Skill_110941_1(CommonSkill):
    """提高自身携带导弹和发射架类装备10点火力值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = EquipTarget(side=1,
                                  target=SelfTarget(master),
                                  equiptype=(AntiMissile, Launcher))
        self.buff = [
            CommonBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            )
        ]


class Skill_110941_2(Skill):
    """随机降低三名敌方单位15回避值、命中值、火力值和装甲值"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = RandomTarget(side=0, num=3)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=-15,
                bias_or_weight=0
            )
        ]


class Skill_110941_3(Skill):
    """对位敌人不参与首轮炮击"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=0, loc=[self.master.loc])
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='not_act_phase',
                phase=FirstShellingPhase
            )
        ]


class Skill_110941_4(CommonSkill):
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


name = '驾束制导'
skill = [Skill_110941_1, Skill_110941_2, Skill_110941_3]
