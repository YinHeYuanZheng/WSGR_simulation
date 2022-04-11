# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 舰R公式

import numpy as np

from src.wsgr.wsgrTimer import Time
from src.wsgr.formulas import *
import src.wsgr.formulas as rform
from src.wsgr.equipment import *
from src.wsgr.ship import Submarine, AntiSubShip

__all__ = ['AllPhase',
           'PreparePhase',
           'BuffPhase',
           'AirPhase',

           'ShellingPhase',
           'FirstShellingPhase',
           'SecondShellingPhase',

           'DaytimePhase',
           'NightPhase']


class AllPhase(Time):
    """战斗阶段总类"""

    def __init__(self, timer, friend, enemy):
        super().__init__(timer)
        self.friend = friend
        self.enemy = enemy

    def start(self):
        pass

    # def get_atk_member(self, side):
    #     """获取可行动单位(目前没有调用该接口的需求，可能需要删除)"""
    #     if side == 1:
    #         fleet = self.friend.ship
    #     else:
    #         fleet = self.enemy.ship
    #
    #     member = fleet.get_member_inphase()
    #     atk_member = []
    #     for tmp_ship in member:
    #         if tmp_ship.get_act_indicator():
    #             atk_member.append(tmp_ship)
    #     return atk_member


class PreparePhase(AllPhase):
    """准备阶段"""

    def __init__(self, timer, friend, enemy):
        super().__init__(timer, friend, enemy)
        self.friend_fleet_speed = None
        self.enemy_fleet_speed = None

    def start(self):
        # 结算影响队友航速、索敌的技能，结算让巴尔
        for tmp_ship in self.friend.ship:
            tmp_ship.run_prepare_skill(self.friend, self.enemy)
        for tmp_ship in self.enemy.ship:
            tmp_ship.run_prepare_skill(self.enemy, self.friend)

        # 计算舰队航速
        self.friend_fleet_speed = self.friend.get_fleet_speed()
        self.enemy_fleet_speed = self.enemy.get_fleet_speed()

        # 索敌
        recon_flag = self.compare_recon()
        # recon_flag = True  # 暂时默认索敌成功
        self.timer.set_recon(recon_flag=recon_flag)

        # 迂回

        # 航向
        direction_flag = self.compare_speed()
        self.timer.set_direction(direction_flag=direction_flag)

    def compare_recon(self):
        sub_num = self.enemy.count(Submarine)
        if sub_num != len(self.enemy.ship):
            friend_recon = self.friend.get_total_status('recon')
            enemy_recon = self.enemy.get_total_status('recon')
            d_recon = friend_recon - enemy_recon

            recon_rate = 0.5 + d_recon * 0.05
            recon_rate = max(0, recon_rate)
            recon_rate = min(1, recon_rate)

            verify = np.random.random()
            if verify <= recon_rate:
                return True
            else:
                return False
        else:
            friend_recon = 0
            for tmp_ship in self.friend.ship:
                if isinstance(tmp_ship, AntiSubShip):
                    friend_recon += tmp_ship.get_final_status('recon')
                    friend_recon += tmp_ship.get_final_status('antisub', equip=False)

            enemy_level = 0
            for tmp_ship in self.enemy.ship:
                enemy_level += tmp_ship.level

            if friend_recon >= enemy_level:
                return True
            else:
                return False

    def compare_speed(self):
        friend_leader_speed = self.friend.ship[0].get_final_status('speed')
        enemy_leader_speed = self.enemy.ship[0].get_final_status('speed')
        d_leader_speed = int(friend_leader_speed - enemy_leader_speed)
        d_fleet_speed = int(self.friend_fleet_speed - self.enemy_fleet_speed)

        # 航向权重，顺序为优同反劣
        if self.timer.direction_flag:
            speed_matrix = np.array([20, 35, 25, 5])
        else:
            speed_matrix = np.array([10, 30, 30, 15])

        speed_matrix[0] += min(d_leader_speed, d_fleet_speed)
        speed_matrix[0] = max(0, speed_matrix[0])
        speed_matrix[1] += d_fleet_speed
        speed_matrix[1] = max(5, speed_matrix[1])
        speed_matrix[2] -= d_leader_speed
        speed_matrix[2] = max(0, speed_matrix[2])
        speed_matrix[3] -= d_fleet_speed
        speed_matrix[3] = max(0, speed_matrix[3])

        speed_matrix = speed_matrix / sum(speed_matrix)
        return np.random.choice([1, 2, 3, 4], p=speed_matrix)


class BuffPhase(AllPhase):
    """buff阶段"""

    def start(self):
        for tmp_ship in self.friend.ship:
            tmp_ship.run_normal_skill(self.friend, self.enemy)
        for tmp_ship in self.enemy.ship:
            tmp_ship.run_normal_skill(self.enemy, self.friend)


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

                # 检查是否存在优先攻击船型对象
                prior = tmp_ship.get_prior_type_target(defend)

                # 轰炸机，发起轰炸攻击
                if isinstance(tmp_equip, Bomber):
                    atk = AirBombAtk(
                        timer=self.timer,
                        atk_body=tmp_ship,
                        def_list=defend,
                        equip=tmp_equip,
                        coef=coef,
                        target=prior,
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
                        target=prior,
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
            hit_back = atk.start()
            if isinstance(hit_back, ATK):
                hit_back.set_coef({'hit_back': True})
                hit_back.start()


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
