# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 舰R公式

import numpy as np

from src.wsgr.wsgrTimer import Time
from src.wsgr.formulas import *
import src.wsgr.formulas as rform
from src.wsgr.equipment import *

__all__ = ['AllPhase',
           'BuffPhase',
           'AirPhase',

           'ShellingPhase',
           'FirstShellingPhase',
           'SecondShellingPhase',

           'NightPhase']


class AllPhase(Time):
    """战斗阶段总类"""

    def __init__(self, timer, friend, enemy):
        super().__init__(timer)
        self.friend = friend
        self.enemy = enemy

    def start(self):
        pass

    def get_atk_member(self, side):
        """获取可行动单位"""
        if side == 1:
            fleet = self.friend.ship
        else:
            fleet = self.enemy.ship

        member = fleet.get_member_inphase()
        atk_member = []
        for tmp_ship in member:
            if tmp_ship.get_act_indicator():
                atk_member.append(tmp_ship)
        return atk_member


class BuffPhase(AllPhase):
    """buff阶段"""

    def start(self):
        for tmp_ship in self.friend.ship:
            for tmp_skill in tmp_ship.skill:
                if tmp_skill.is_active(self.friend, self.enemy):
                    tmp_skill.activate(self.friend, self.enemy)
        for tmp_ship in self.enemy.ship:
            for tmp_skill in tmp_ship.skill:
                if tmp_skill.is_active(self.enemy, self.friend):
                    tmp_skill.activate(self.enemy, self.friend)


class DaytimePhase(AllPhase):
    """昼战阶段"""
    pass


class AirPhase(DaytimePhase):
    """航空战阶段"""

    def start(self):
        # 检查可参与航空战的对象
        atk_friend = self.friend.get_act_member_inphase()
        atk_enemy = self.enemy.get_act_member_inphase()
        # 检查可被航空攻击的对象
        def_friend = self.friend.get_atk_target(atk_type=AirAtk)
        def_enemy = self.enemy.get_atk_target(atk_type=AirAtk)

        # 如果不存在可行动对象或可攻击对象，结束本阶段
        if (len(atk_friend) and len(def_enemy)) or \
                (len(atk_enemy) and len(def_friend)):
            pass
        else:
            return

        # 检查双方攻击性飞机, 都为0不进行航空战
        atk_plane_friend = self.get_atk_plane(side=1)
        atk_plane_enemy = self.get_atk_plane(side=0)
        if not atk_plane_friend and not atk_plane_enemy:
            return

        # 计算双方制空
        aerial_friend = rform.get_fleet_aerial(atk_friend)
        aerial_enemy = rform.get_fleet_aerial(atk_enemy)
        # 制空结果, 从空确到空丧分别为1-5
        air_con_flag = rform.compare_aerial(aerial_friend, aerial_enemy)
        # 制空均为0时特殊情况, 检查双方攻击性飞机
        if aerial_friend == 0 and aerial_enemy == 0:
            if atk_plane_friend and not atk_plane_enemy:
                air_con_flag = 1
            elif atk_plane_friend and atk_plane_enemy:
                air_con_flag = 3
            elif not atk_plane_friend and atk_plane_enemy:
                air_con_flag = 5
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
            fall_rand = np.random.uniform(*fall_coef)  # 每艘船固定一个制空击坠随机数
            flightlimit = rform.get_flightlimit(tmp_ship)  # 放飞限制
            for tmp_equip in tmp_ship.equipment:
                coef = {}  # 公式参数

                # 检查该装备是否为参与航空战的飞机
                if not isinstance(tmp_equip, Plane):
                    continue
                if isinstance(tmp_equip, ScoutPLane):  # 侦察机不参与航空战
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
                if isinstance(tmp_equip, Fighter):
                    tmp_equip.fall(air_con_fall)  # 最大击坠量可超过实际放飞量（存在洗甲板）
                    continue

                # 轰炸机，发起轰炸攻击
                elif isinstance(tmp_equip, Bomber):
                    atk = AirBombAtk(
                        timer=self.timer,
                        atk_body=tmp_ship,
                        def_list=defend,
                        equip=tmp_equip,
                        coef=coef,
                    )
                    atk.start()
                    anti_num = atk.get_coef('anti_num')

                # 攻击机，发起鱼雷轰炸攻击
                elif isinstance(tmp_equip, DiveBomber):
                    atk = AirDiveAtk(
                        timer=self.timer,
                        atk_body=tmp_ship,
                        def_list=defend,
                        equip=tmp_equip,
                        coef=coef,
                    )
                    atk.start()
                    anti_num = atk.get_coef('anti_num')

    def get_atk_plane(self, side):
        if side == 1:
            fleet = self.friend.ship
        else:
            fleet = self.enemy.ship

        for tmp_ship in fleet:
            for tmp_equip in tmp_ship.equipment:
                if isinstance(tmp_equip, (Fighter, Bomber, DiveBomber)):
                    if tmp_equip.load > 0:
                        return True
        return False


class ShellingPhase(DaytimePhase):
    """炮击战"""
    def start(self):
        # 检查可参与炮击战的对象
        atk_friend = self.friend.get_member_inphase()
        atk_enemy = self.enemy.get_member_inphase()

        # 如果双方均不存在可行动对象，结束本阶段
        if not len(atk_friend) and not len(atk_enemy):
            return

        # 排列炮序
        ordered_friend = self.get_order(atk_friend)
        ordered_enemy = self.get_order(atk_enemy)

        # 按照炮序依次行动
        for i in range(6):
            if i < len(ordered_friend):
                self.normal_atk(ordered_friend[i], self.enemy)

            if i < len(ordered_enemy):
                self.normal_atk(ordered_enemy[i], self.friend)

    def get_order(self, fleet):
        """炮序"""
        fleet.sort(key=lambda x: x.loc)
        return fleet

    def normal_atk(self, source, target_fleet):
        if not source.get_act_indicator():
            return

        atk_list = source.raise_atk(target_fleet)
        for atk in atk_list:
            atk.start()


class FirstShellingPhase(ShellingPhase):
    """首轮炮击"""

    def get_order(self, fleet):
        """炮序"""
        base_order = [5, 6, 4, 3, 2, 1]
        fleet.sort(key=lambda x: (-x.get_range(), base_order.index(x.loc)))
        return fleet


class SecondShellingPhase(ShellingPhase):
    """次轮炮击"""
    pass


class NightPhase(AllPhase):
    """夜战"""
    pass
