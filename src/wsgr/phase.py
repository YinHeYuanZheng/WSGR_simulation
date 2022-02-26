# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 舰R公式

import random
import numpy as np
# import sys
# sys.path.append(r'.\wsgr')

from .formulas import *
from . import formulas as rform
from . import equipment as requip
from .wsgrTimer import Time

__all__ = ['AllPhase',
           'BuffPhase',
           'AirPhase',

           'ShellingPhase',
           'FirstShellingPhase',
           'SecondShellingPhase',
           ]


class AllPhase(Time):
    """战斗阶段总类"""

    def start(self):
        pass


class BuffPhase(AllPhase):
    """buff阶段"""

    def __init__(self, friend, enemy):
        super().__init__()
        self.friend = friend
        self.enemy = enemy

    def start(self):
        for tmp_ship in self.friend.ship:
            for tmp_skill in tmp_ship.skill:
                if tmp_skill.is_active(self.friend, self.enemy):
                    tmp_skill.activate(self.friend, self.enemy)
        for tmp_ship in self.enemy.ship:
            for tmp_skill in tmp_ship.skill:
                if tmp_skill.is_active(self.enemy, self.friend):
                    tmp_skill.activate(self.enemy, self.friend)


class AirPhase(AllPhase):
    """航空战阶段"""

    def __init__(self, friend, enemy):
        super().__init__()
        self.friend = friend
        self.enemy = enemy

    def start(self):
        # 检查可参与航空战的对象
        atk_friend = self.friend.get_member_inphase()
        atk_enemy = self.enemy.get_member_inphase()
        # 检查可被航空攻击的对象
        def_friend = self.friend.get_target(AirAtk)
        def_enemy = self.enemy.get_target(AirAtk)

        # 如果不存在可行动对象或可攻击对象，结束本阶段
        if (len(atk_friend) and len(def_enemy)) or \
                (len(atk_enemy) and len(def_friend)):
            pass
        else:
            return

        # 计算双方制空
        aerial_friend = rform.get_fleet_aerial(atk_friend)
        aerial_enemy = rform.get_fleet_aerial(atk_enemy)
        # 制空结果
        air_con_flag = rform.compare_aerial(aerial_friend, aerial_enemy)
        self.timer.set_air_con(air_con_flag)

        # 航空轰炸阶段
        self.air_strike(atk_friend, def_enemy, aerial_enemy, side=1)
        self.air_strike(atk_enemy, def_friend, aerial_friend, side=0)

    def air_strike(self, attack, defend, aerial, side):
        """

        :param attack: 攻击方对象
        :param defend: 被攻击对象
        :param aerial: 被攻击方制空
        :param side: 1: friend; 0: enemy
        :return:
        """
        fall_coef, air_con_coef = rform.get_air_coef(self.timer.air_con_flag,
                                                     side)  # 制空击坠系数，航空战系数

        anti_num = [0] * len(defend)  # 迎击序数
        total_plane_rest = rform.get_total_plane_rest(attack)  # 总剩余载机量

        for tmp_ship in attack:
            fall_rand = random.uniform(*fall_coef)  # 每艘船固定一个制空击坠随机数
            flightlimit = rform.get_flightlimit(tmp_ship)  # 放飞限制
            for tmp_equip in tmp_ship.equipment:
                coef = {}  # 公式参数

                # 检查该装备是否为参与航空战的飞机
                if not isinstance(tmp_equip, requip.Plane):
                    continue
                if isinstance(tmp_equip, requip.ScoutPLane):  # 侦察机不参与航空战
                    continue

                # 检查该飞机载量是否不为0
                if tmp_equip.load == 0:
                    continue

                # 实际放飞值为机库剩余量与放飞限制的较小值
                actual_flight = min(tmp_equip.load, flightlimit)
                coef['actual_flight'] = actual_flight

                # 制空击坠
                air_con_fall = rform.get_air_con_fall(
                    tmp_equip.load,
                    total_plane_rest,
                    aerial,
                    fall_rand
                )
                coef['air_con_fall'] = air_con_fall

                # 攻击结算前参数生成
                coef['anti_num'] = anti_num
                coef['air_con_coef'] = air_con_coef

                # 战斗机仅计算制空击坠就结束
                if isinstance(tmp_equip, requip.Fighter):
                    tmp_equip.fall(air_con_fall)  # 最大击坠量可超过实际放飞量（存在洗甲板）
                    continue

                # 轰炸机，发起轰炸攻击
                elif isinstance(tmp_equip, requip.Bomber):
                    atk = AirBombAtk(
                        atk_body=tmp_ship,
                        def_list=defend,
                        equip=tmp_equip,
                        coef=coef,
                        atk_form=self.friend.form if side == 1 else self.enemy.form,
                        def_form=self.enemy.form if side == 1 else self.friend.form
                    )
                    atk.start()
                    anti_num = atk.get_coef('anti_num')

                # 攻击机，发起鱼雷轰炸攻击
                elif isinstance(tmp_equip, requip.DiveBomber):
                    atk = AirDiveAtk(
                        atk_body=tmp_ship,
                        def_list=defend,
                        equip=tmp_equip,
                        coef=coef,
                        atk_form=self.friend.form if side == 1 else self.enemy.form,
                        def_form=self.enemy.form if side == 1 else self.friend.form
                    )
                    atk.start()
                    anti_num = atk.get_coef('anti_num')


class ShellingPhase(AllPhase):
    """炮击战"""
    pass


class FirstShellingPhase(AllPhase):
    """首轮炮击"""
    pass


class SecondShellingPhase(AllPhase):
    """次轮炮击"""
    pass
