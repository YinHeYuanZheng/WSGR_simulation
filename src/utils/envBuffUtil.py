# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 环境加成

import os
import pandas as pd
from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *
import src.wsgr.ship as rship
import src.wsgr.phase as rphase


class AllTarget(Target):
    """针对双方全体(可指定筛选类型)"""

    def __init__(self, side=None, target: Target = None):
        super().__init__(side)
        self.target = target

    def get_target(self, friend, enemy):
        if self.target is not None:
            target_1 = self.target.get_target(friend, enemy)
            target_0 = self.target.get_target(enemy, friend)
            return target_1 + target_0
        else:
            if isinstance(friend, Fleet):
                friend = friend.ship
            if isinstance(enemy, Fleet):
                enemy = enemy.ship
            return friend + enemy


class EnvSkill_1(Skill):
    """猪飞：大型船伤害+60%"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=LargeShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.6
            )
        ]


class EnvSkill_2(Skill):
    """猪飞：中型船伤害+60%"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=MidShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.6
            )
        ]


class EnvSkill_3(Skill):
    """猪飞：小型船伤害+60%"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=SmallShip)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=10,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.1,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=0.6
            )
        ]


class EnvSkill_4(Skill):
    """航巡全阶段必中"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=CAV)
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='must_hit',
                phase=AllPhase
            )
        ]


class Engineer_SS(Skill):
    """SS工程局"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=SS)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
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
            ),
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.03,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=TorpedoPhase,
                value=0.05
            )
        ]


class Engineer_DD(Skill):
    """DD工程局"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=DD)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
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
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antisub',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='luck',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=SecondTorpedoPhase,
                value=0.05
            )
        ]


class Engineer_ASDG(Skill):
    """ASDG工程局"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=ASDG)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
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
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.03,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=FirstMissilePhase,
                value=0.05
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AirPhase,
                value=-0.1
            )
        ]


class Engineer_CL(Skill):
    """CL工程局"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=CL)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='torpedo',
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
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antisub',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='luck',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=SecondTorpedoPhase,
                value=0.05
            )
        ]


class Engineer_BB(Skill):
    """BB工程局"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=BB)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
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
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.03,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AirPhase,
                value=-0.1
            )
        ]


class Engineer_BC(Skill):
    """BC工程局"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=BC)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
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
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.03,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=ShellingPhase,
                value=0.05
            )
        ]


class Engineer_BBG(Skill):
    """BBG工程局"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=BBG)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
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
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.03,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=FirstMissilePhase,
                value=0.05
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AirPhase,
                value=-0.1
            )
        ]


class Engineer_BG(Skill):
    """BG工程局"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=BG)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
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
            ),
            StatusBuff(
                timer=timer,
                name='recon',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=0.03,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=SecondMissilePhase,
                value=0.05
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=ShellingPhase,
                value=-0.1
            )
        ]


class Collection_C_fire(Skill):
    """C国火力+5 +3"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CountryTarget(side=1, country='C')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=8,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='luck',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
        ]


class Collection_SS_torpedo(Skill):
    """SS鱼雷+2 +3"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=SS)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
        ]


class Collection_BB_fire(Skill):
    """BB火力+2 +1"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=BB)
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=3,
                bias_or_weight=0
            ),
        ]


class Collection_F_BB_fire(Skill):
    """F国BB火力+2"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                TypeTarget(side=1, shiptype=BB),
                CountryTarget(side=1, country='F')
            ]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=2,
                bias_or_weight=0
            ),
        ]


class Collection_U_torpedo(Skill):
    """U国鱼雷+2"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CountryTarget(side=1, country='U')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=2,
                bias_or_weight=0
            )
        ]


class Dish_C_fire(Skill):
    """C国火力+11"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CountryTarget(side=1, country='C')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=11,
                bias_or_weight=0
            )
        ]


class Dish_F_BB_fire(Skill):
    """F国BB火力+7"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                TypeTarget(side=1, shiptype=BB),
                CountryTarget(side=1, country='F')
            ]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=7,
                bias_or_weight=0
            ),
        ]


class Dish_E_fire(Skill):
    """E国火力+5"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CountryTarget(side=1, country='E')
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            ),
        ]


class Dish_G_finaldamage(Skill):
    """G国鱼雷战终伤+5%"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CountryTarget(side=1, country='G')
        self.buff = [
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=SecondTorpedoPhase,
                value=0.05
            )
        ]


class Car_Large_fire(Skill):
    """大型船火力+5"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                TypeTarget(side=1, shiptype=LargeShip),
                CountryTarget(side=1, country='CF')
            ]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


class Car_Small_torpedo(Skill):
    """小型船鱼雷+5"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CombinedTarget(
            side=1,
            target_list=[
                TypeTarget(side=1, shiptype=SmallShip),
                CountryTarget(side=1, country='U')
            ]
        )
        self.buff = [
            StatusBuff(
                timer=timer,
                name='torpedo',
                phase=AllPhase,
                value=5,
                bias_or_weight=0
            )
        ]


class Event_G_buff(Skill):
    """G国无视战损"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CountryTarget(side=1, country='G')
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase
            ),
            # FinalDamageBuff(
            #     timer=timer,
            #     name='final_damage_buff',
            #     phase=AllPhase,
            #     value=0.3,
            # )
        ]


class Event_U_buff(Skill):
    """U国无视战损"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CountryTarget(side=1, country='U')
        self.buff = [
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase
            )
        ]


class Event_DD_FirstTorpedo(Skill):
    """DD开幕雷"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = TypeTarget(side=1, shiptype=DD)
        self.buff = [
            ActPhaseBuff(
                timer=timer,
                name='act_phase',
                phase=TorpedoPhase,
            )
        ]


class Event_SpecialBuff_Skill(Skill):
    """活动彩蛋船专属buff(圣地亚哥)"""
    def __init__(self, timer):
        super().__init__(timer, master=None)
        self.target = CidTarget(side=1, cid_list=['10157'])
        self.buff = [
            StatusBuff(
                timer=timer,
                name='fire',
                phase=AllPhase,
                value=53,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='accuracy',
                phase=AllPhase,
                value=53,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='armor',
                phase=AllPhase,
                value=53,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='evasion',
                phase=AllPhase,
                value=106,
                bias_or_weight=0
            ),
            StatusBuff(
                timer=timer,
                name='antiair',
                phase=AllPhase,
                value=106,
                bias_or_weight=0
            ),
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=.53,
                bias_or_weight=0
            ),
            FinalDamageBuff(
                timer=timer,
                name='final_damage_buff',
                phase=AllPhase,
                value=2.18
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_damaged',
                phase=AllPhase
            ),
            SpecialBuff(
                timer=timer,
                name='ignore_supply',
                phase=AllPhase
            ),
        ]


class Normal_map9_lock_buff(Skill):
    """9图解封锁buff"""
    def __init__(self, timer):
        class LeaderSurviveBuff(FinalDamageBuff):
            def is_active(self, *args, **kwargs):
                leader = self.master.master.ship[0]
                return leader.damaged <= 3

        super().__init__(timer, master=None)
        self.target = LocTarget(side=0, loc=[2,3,4,5,6])
        self.buff = [
            LeaderSurviveBuff(
                timer=timer,
                name='final_damage_debuff',
                phase=AllPhase,
                value=-0.1
            )
        ]


def dynamic_init(self, timer, config: dict):
    super(self.__class__, self).__init__(timer, master=None)

    # --- Target 构建 ---
    target_list = []
    country = config.get('country', '')
    if country != '':
        target_list.append(
            CountryTarget(side=1, country=country)
        )

    shiptype = config.get('shiptype', '')
    if shiptype != '':
        types = [getattr(rship, s) for s in shiptype.split(',')]
        if types:
            target_list.append(
                TypeTarget(side=1, shiptype=tuple(types))
            )

    if len(target_list) > 1:
        self.target = CombinedTarget(side=1, target_list=target_list)
    elif len(target_list) == 1:
        self.target = target_list[0]
    else:
        self.target = Target(side=1)

    # --- Buff 构建 ---
    self.buff = []

    # A. 基础属性 (StatusBuff)
    status_name_list = ['fire', 'torpedo', 'armor', 'antiair', 'antisub',
                        'accuracy', 'evasion', 'recon', 'luck'
                        ]
    for name in status_name_list:
        val = config.get(name)
        if val != '':
            self.buff.append(
                StatusBuff(
                    timer=timer,
                    name=name,
                    phase=AllPhase,
                    value=float(val),
                    bias_or_weight=0
                )
            )

    # B. 暴击 (CoeffBuff)
    crit_val = config.get('crit')
    if crit_val != '':
        self.buff.append(
            CoeffBuff(
                timer=timer,
                name='crit',
                phase=AllPhase,
                value=float(crit_val),
                bias_or_weight=0
            )
        )

    # C. 伤害加成/减免 (FinalDamageBuff)
    for name in ['final_damage_buff', 'final_damage_debuff']:
        val = config.get(name)
        if val == '':
            continue

        # 将全角标点符号转为半角
        val = val.replace('：', ':')
        val = val.replace('；', ';')

        # 尝试解析字典格式，如 ShellingPhase:0.1;
        try:
            val_data = {k: float(v) for k, v in (item.split(':') for item in val.split(';'))}
        except:
            raise ValueError(f'{type(self).__name__}: {name} 填写格式错误')
        if isinstance(val_data, dict):
            for p_name, p_val in val_data.items():
                # 使用 getattr 动态获取阶段
                assert p_name in rphase.__all__, f'{type(self).__name__}: {name} 阶段填写错误'
                phase = getattr(rphase, p_name)
                self.buff.append(
                    FinalDamageBuff(
                        timer=timer,
                        name=name,
                        phase=phase,
                        value=p_val
                    )
                )

    # D. 特殊效果 (SpecialBuff)
    for name in ['ignore_damaged', 'ignore_supply', 'must_hit', 'act_phase']:
        val = config.get(name)
        if val == '':
            continue
        # 如果单元格填了 TRUE/1 等
        if val in ['1', 'TRUE', 'True']:
            assert name not in ['must_hit', 'act_phase'], f'{type(self).__name__}: {name} 填写格式错误'
            self.buff.append(
                SpecialBuff(
                    timer=timer,
                    name=name,
                    phase=AllPhase
                )
            )
        else:
            try:
                phase = getattr(rphase, val)
            except:
                raise Exception(f'{type(self).__name__}: {name} 阶段填写错误')
            self.buff.append(
                SpecialBuff(
                    timer=timer,
                    name=name,
                    phase=phase
                )
            )


def create_skill_class(cls, config):
    """
    使用 type() 动态创建一个类，就像写了 class Name(Skill): ... 一样
    """

    # 将当前的配置行固化到初始化函数中
    def wrapped_init(self, timer):
        dynamic_init(self, timer, config)

    # 参数：类名，父类元组，属性字典
    return type(cls, (Skill,), {"__init__": wrapped_init})


def load_env_buffs(file_path):
    """从Excel读取并返回技能实例列表"""
    COLUMN_MAP = {
        '名称': 'name',
        '国籍': 'country',
        '舰种': 'shiptype',
        '生效': 'valid',
        '火力': 'fire',
        '鱼雷': 'torpedo',
        '装甲': 'armor',
        '对空': 'antiair',
        '对潜': 'antisub',
        '命中': 'accuracy',
        '回避': 'evasion',
        '索敌': 'recon',
        '幸运': 'luck',
        '暴击': 'crit',
        '伤害提升': 'final_damage_buff',
        '受伤降低': 'final_damage_debuff',
        '无视战损': 'ignore_damaged',
        '无视补给': 'ignore_supply',
        '必中': 'must_hit',
        '参与阶段': 'act_phase',
    }

    df = pd.read_excel(file_path, keep_default_na=False, dtype=str)
    df.rename(columns=COLUMN_MAP, inplace=True)
    env_skills = []
    for i, row in df.iterrows():
        config = row.to_dict()
        # 检查buff是否生效
        if not bool(config.get('valid')):
            continue
        name = config.get('name', f'DynamicSkill_{i+1}').replace(' ', '_')
        # 过滤非法字符确保符合Python类名规范(支持字符：字母、数字、下划线)
        safe_class_name = "".join(c for c in name if c.isalnum() or c == "_")

        # 创建类(不是实例!)
        SkillClass = create_skill_class(safe_class_name, config)
        env_skills.append(SkillClass)

    return env_skills


# todo 工程局、藏品、赛车、餐厅、环境buff等可从config设置
curDir = os.path.dirname(__file__)
srcDir = os.path.dirname(curDir)
dependDir = os.path.join(os.path.dirname(srcDir), 'depend')
data_file = os.path.join(dependDir, r'environment/environment.xlsx')
env = load_env_buffs(data_file)
