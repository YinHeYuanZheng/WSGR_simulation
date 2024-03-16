# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 鹰潭

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队舰船索敌值增加4点、对空值增加20点，C国舰船获得双倍效果。
昼战阶段自身攻击时有50%概率无视目标装甲并增加50%伤害，队伍中每有1艘C国舰船都会增加10%概率。
自身装备的发射器会视为反潜装备，其索敌值视为对潜值。"""


class Skill_102871_1(PrepSkill):
    """全队舰船索敌值增加4点，C国舰船获得双倍效果。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=4,
                bias_or_weight=0,
            ),
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                if tmp_target.status['country'] == 'C':
                    tmp_buff.value *= 2
                tmp_target.add_buff(tmp_buff)


class Skill_102871_2(Skill):
    """全队舰船对空值增加20点，C国舰船获得双倍效果。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = Target(side=1)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=20,
                bias_or_weight=0,
            ),
        ]

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                if tmp_target.status['country'] == 'C':
                    tmp_buff.value *= 2
                tmp_target.add_buff(tmp_buff)


class Skill_102871_3(Skill):
    """昼战阶段自身攻击时有50%概率无视目标装甲并增加50%伤害，
    队伍中每有1艘C国舰船都会增加10%概率。"""

    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            AtkHitBuff(
                timer=timer,
                name='give_atk',
                phase=DaytimePhase,
                buff=[
                    DuringAtkBuff(
                        timer=timer,
                        name='ignore_armor',
                        phase=DaytimePhase,
                        value=-1,
                        bias_or_weight=1,
                    ),
                    DuringAtkBuff(
                        timer=timer,
                        name='final_damage_buff',
                        phase=DaytimePhase,
                        value=0.5,
                        bias_or_weight=2,
                    ),
                ],
                side=1,
                rate=.5
            )
        ]

    def activate(self, friend, enemy):
        num = len(CountryTarget(side=1, country='C'
                                ).get_target(friend, enemy))
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_buff.rate += .1 * num
                tmp_target.add_buff(tmp_buff)


class Skill_102871_4(CommonSkill):
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
                recon = tmp_equip.status.get('recon', 0)
                new_equip.set_status('antisub', recon)
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


name = '南沙功臣'
skill = [Skill_102871_1, Skill_102871_2, Skill_102871_3, Skill_102871_4]
