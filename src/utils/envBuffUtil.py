# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 环境加成

from src.wsgr.skill import *
from src.wsgr.ship import *
from src.wsgr.phase import *


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


# todo 工程局、藏品、赛车、餐厅、环境buff等可从config设置
# env = [Engineer_SS, Engineer_DD, Engineer_ASDG, Engineer_CL,
#        Engineer_BB, Engineer_BC, Engineer_BG, Engineer_BBG,
#
#        Collection_C_fire, Collection_SS_torpedo, Collection_U_torpedo,
#        Collection_BB_fire, Collection_F_BB_fire,
#
#        Dish_C_fire, Dish_F_BB_fire, Dish_G_finaldamage,
#        Dish_E_fire,
#
#        Car_Large_fire, Car_Small_torpedo]
env = []
