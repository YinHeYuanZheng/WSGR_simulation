# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 不惧-1

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *

"""全队大巡、防巡和防驱增加30%护甲穿透，增加20点回避值与对空值。
自身攻击时降低敌方50%的回避值，并造成敌方50%回避值的额外伤害。
战斗时自身射程增加2档，我方舰队旗舰射程增加1档，敌方舰队旗舰射程降低2档。
自身装备的发射器会视为反潜装备，其索敌值视为对潜值。"""


class Skill_105591_1(Skill):
    """全队大巡、防巡和防驱增加30%护甲穿透，增加20点回避值与对空值。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = TypeTarget(side=1, shiptype=(BG, CG, AADG))
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='pierce_coef',
                phase=AllPhase,
                value=0.3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=20,
                bias_or_weight=0
            ),
        ]


class Skill_105591_2(Skill):
    """自身攻击时降低敌方50%的回避值，并造成敌方50%回避值的额外伤害。"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            CoeffBuff(
                timer=timer,
                name='ignore_evasion',
                phase=AllPhase,
                value=-0.5,
                bias_or_weight=1
            ),
            EvasionExtraDamage(
                timer=timer,
                name='extra_damage',
                phase=AllPhase,
                value=0.5,
                bias_or_weight=0
            ),
        ]


class EvasionExtraDamage(AtkBuff):
    def change_value(self, *args, **kwargs):
        try:
            atk = kwargs['atk']
        except:
            atk = args[0]
        self.value = np.ceil(atk.target.get_final_status('evasion') * 0.5)


class Skill_105591_3(Skill):
    """自身射程增加2档"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = SelfTarget(master)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range_buff',
                phase=AllPhase,
                value=2,
                bias_or_weight=0
            ),
        ]


class Skill_105591_4(Skill):
    """我方舰队旗舰射程增加1档"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=1, loc=[1])
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range_buff',
                phase=AllPhase,
                value=1,
                bias_or_weight=0
            ),
        ]


class Skill_105591_5(Skill):
    """敌方舰队旗舰射程降低2档"""
    def __init__(self, timer, master):
        super().__init__(timer, master)
        self.target = LocTarget(side=0, loc=[1])
        self.buff = [
            StatusBuff(
                timer=timer,
                name='range_buff',
                phase=AllPhase,
                value=-2,
                bias_or_weight=0
            ),
        ]


class Skill_105591_6(CommonSkill):
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


name = '先驱者'
skill = [Skill_105591_1, Skill_105591_2, Skill_105591_3,
         Skill_105591_4, Skill_105591_5, Skill_105591_6]
