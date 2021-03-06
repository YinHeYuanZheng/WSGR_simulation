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

           'MissilePhase',
           'FirstMissilePhase',
           'SecondMissilePhase',

           'AntiSubPhase',

           'TorpedoPhase',
           'FirstTorpedoPhase',
           'SecondTorpedoPhase',

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

    def start(self):
        # 索敌
        recon_flag = self.compare_recon()
        # recon_flag = True  # 暂时默认索敌成功
        self.timer.set_recon(recon_flag=recon_flag)

        # 迂回

        # 结算影响队友航速、索敌的技能，结算让巴尔
        self.timer.run_prepare_skill(self.friend, self.enemy)
        for tmp_ship in self.friend.ship:
            tmp_ship.run_prepare_skill(self.friend, self.enemy)
        for tmp_ship in self.enemy.ship:
            tmp_ship.run_prepare_skill(self.enemy, self.friend)

        # 航向
        direction_flag = self.compare_speed()
        self.timer.set_direction(direction_flag=direction_flag)

    def compare_recon(self):
        sub_num = self.enemy.count(Submarine)
        if sub_num != len(self.enemy.ship):
            friend_recon = self.friend.status['recon']
            enemy_recon = self.enemy.status['recon']
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
            friend_recon = self.friend.status['antisub_recon']
            enemy_level = 0
            for tmp_ship in self.enemy.ship:
                enemy_level += tmp_ship.level

            if friend_recon >= enemy_level:
                return True
            else:
                return False

    def compare_speed(self):
        # 旗舰航速差
        friend_leader_speed = self.friend.ship[0].get_final_status('speed')
        enemy_leader_speed = self.enemy.ship[0].get_final_status('speed')
        d_leader_speed = int(friend_leader_speed - enemy_leader_speed)

        # 舰队航速差
        friend_fleet_speed = self.friend.get_fleet_speed()
        enemy_fleet_speed = self.enemy.get_fleet_speed()
        d_fleet_speed = int(friend_fleet_speed - enemy_fleet_speed)

        # 航向权重，顺序为优同反劣
        if self.timer.recon_flag:
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
        self.timer.run_normal_skill(self.friend, self.enemy)
        for tmp_ship in self.friend.ship:
            tmp_ship.run_normal_skill(self.friend, self.enemy)
            tmp_ship.run_strategy()
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
        def_friend = self.friend.get_atk_target(atk_type=AirStrikeAtk)
        def_enemy = self.enemy.get_atk_target(atk_type=AirStrikeAtk)

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

        # 航空轰炸阶段，先结算我方
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
                if prior is not None:
                    def_list = prior
                else:
                    def_list = defend

                # 轰炸机，发起轰炸攻击
                if isinstance(tmp_equip, Bomber):
                    atk = AirBombAtk(
                        timer=self.timer,
                        atk_body=tmp_ship,
                        def_list=def_list,
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
                        def_list=def_list,
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


class MissilePhase(DaytimePhase):
    """导弹战"""
    def start(self):
        # 检查可参与导弹战的对象
        atk_friend = self.friend.get_act_member_inphase()
        atk_enemy = self.enemy.get_act_member_inphase()
        # 检查可被导弹攻击的对象
        def_friend = self.friend.get_atk_target(atk_type=MissileAtk)
        def_enemy = self.enemy.get_atk_target(atk_type=MissileAtk)

        # 如果不存在可行动对象或可攻击对象，结束本阶段
        if (len(atk_friend) and len(def_enemy)) or \
                (len(atk_enemy) and len(def_friend)):
            pass
        else:
            return

        # 按照站位依次行动，先结算我方
        self.missile_strike(atk_friend, def_enemy)
        atk_enemy = self.enemy.get_act_member_inphase()  # 重新检查敌方可行动对象
        self.missile_strike(atk_enemy, def_friend)

    def missile_strike(self, attack, defend):
        pass

    def get_atk_missile(self, shiplist):
        """获取反舰导弹"""
        msl_list = []
        for tmp_ship in shiplist:
            for tmp_equip in tmp_ship.equipment:
                if isinstance(tmp_equip, NormalMissile) and tmp_equip.load > 0:
                    msl_list.append(tmp_equip)
        msl_list.sort(key=lambda x: (x.get_final_status('missile_atk'),
                                     -(x.enum + 4 * x.master.loc))
                      )  # 按照突防从小到大+顺位倒序排序
        return msl_list

    def get_def_missile(self, shiplist):
        """获取防空导弹"""
        from src.wsgr.ship import DefMissileShip
        msl_list = []
        for tmp_ship in shiplist:
            if isinstance(tmp_ship, DefMissileShip) and tmp_ship.check_missile():
                for tmp_equip in tmp_ship.equipment:
                    if isinstance(tmp_equip, AntiMissile) and tmp_equip.load > 0:
                        msl_list.append(tmp_equip)
        return msl_list


class FirstMissilePhase(MissilePhase):
    """开幕导弹"""

    def missile_strike(self, attack, defend):
        atk_missile_list = self.get_atk_missile(attack)  # 反舰导弹
        def_missile_list = self.get_def_missile(defend)  # 防空导弹

        total_msl_def = sum([msl.get_final_status('missile_def')
                             for msl in def_missile_list])  # 总拦截

        for tmp_atk_msl in atk_missile_list:
            single_msl_atk = tmp_atk_msl.get_final_status('missile_atk')

            # 拦截条件：总拦截大于突防，且存在可用防空导弹
            if total_msl_def >= single_msl_atk and len(def_missile_list):
                total_msl_def -= single_msl_atk
                tmp_atk_msl.load -= 1
                tmp_def_msl = def_missile_list.pop(0)
                tmp_def_msl.load -= 1
            else:
                atk = MissileAtk(
                    timer=self.timer,
                    atk_body=tmp_atk_msl.master,
                    def_list=defend,
                    equip=tmp_atk_msl
                )
                atk.start()
                tmp_atk_msl.load -= 1


class SecondMissilePhase(MissilePhase):
    """闭幕导弹"""
    def missile_strike(self, attack, defend):
        missile_list = self.get_def_missile(attack)  # 防空导弹
        for tmp_atk_msl in missile_list:
            atk = MissileAtk(
                timer=self.timer,
                atk_body=tmp_atk_msl.master,
                def_list=defend,
                equip=tmp_atk_msl
            )
            atk.start()
            tmp_atk_msl.load -= 1


class AntiSubPhase(DaytimePhase):
    """先制反潜"""

    def start(self):
        # 检查可参与先制反潜的对象
        atk_friend = self.friend.get_act_member_inphase()
        atk_enemy = self.enemy.get_act_member_inphase()
        # 检查可被反潜攻击的对象
        def_friend = self.friend.get_atk_target(atk_type=AntiSubAtk)
        def_enemy = self.enemy.get_atk_target(atk_type=AntiSubAtk)

        # 如果不存在可行动对象或可攻击对象，结束本阶段
        if (len(atk_friend) and len(def_enemy)) or \
                (len(atk_enemy) and len(def_friend)):
            pass
        else:
            return

        # 按照站位依次行动，先结算我方
        self.anti_sub_strike(atk_friend, def_enemy)
        self.anti_sub_strike(atk_enemy, def_friend)

    def anti_sub_strike(self, attack, defend):
        for tmp_ship in attack:
            # 发起反潜攻击
            atk = tmp_ship.anti_sub_atk(
                timer=self.timer,
                atk_body=self,
                def_list=defend,
            )
            atk.start()

            # 去除被击沉目标
            if atk.target.damaged == 4:
                defend.remove(atk.target)


class TorpedoPhase(DaytimePhase):
    """鱼雷战"""

    def start(self):
        # 检查可参与先制鱼雷的对象
        atk_friend = self.friend.get_act_member_inphase()
        atk_enemy = self.enemy.get_act_member_inphase()
        # 检查可被鱼雷攻击的对象
        def_friend = self.friend.get_atk_target(atk_type=TorpedoAtk)
        def_enemy = self.enemy.get_atk_target(atk_type=TorpedoAtk)

        # 如果不存在可行动对象或可攻击对象，结束本阶段
        if (len(atk_friend) and len(def_enemy)) or \
                (len(atk_enemy) and len(def_friend)):
            pass
        else:
            return

        # 按照站位依次行动，先结算我方
        self.torpedo_strike(atk_friend, def_enemy)
        atk_enemy = self.enemy.get_act_member_inphase()  # 重新检查敌方可行动对象
        self.torpedo_strike(atk_enemy, def_friend)

    def torpedo_strike(self, attack, defend):
        for tmp_ship in attack:
            # 检查是否存在优先攻击船型对象
            prior = tmp_ship.get_prior_type_target(defend)
            if prior is not None:
                def_list = prior
            else:
                def_list = defend

            # 检查是否有多发鱼雷技能
            if tmp_ship.get_special_buff('multi_torpedo_attack'):
                num = 2
            else:
                num = 1

            # 雁行雷击

            # 发起鱼雷攻击
            for i in range(num):
                atk = TorpedoAtk(
                    timer=self.timer,
                    atk_body=tmp_ship,
                    def_list=def_list,
                )
                atk.start()


class FirstTorpedoPhase(TorpedoPhase):
    """先制鱼雷"""
    pass


class SecondTorpedoPhase(TorpedoPhase):
    """闭幕鱼雷"""
    pass


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

    def get_order(self, fleet: list):
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
                # hit_back_list.append(hit_back)  # todo 反击结算放在所有攻击结束后
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

    def start(self):
        act_flag_0 = False  # 记录夜战内是否有单位行动过

        # 按照站位顺序依次行动
        for i in range(6):
            if i < len(self.friend.ship):
                act_flag_1 = self.night_atk(self.friend.ship[i], self.enemy)
                act_flag_0 = act_flag_0 or act_flag_1

            if i < len(self.enemy.ship):
                act_flag_1 = self.night_atk(self.enemy.ship[i], self.friend)
                act_flag_0 = act_flag_0 or act_flag_1

        if act_flag_0:  # 进行过夜战，扣除对应弹药
            for tmp_ship in self.friend.ship:
                tmp_ship.supply_ammo = max(0., tmp_ship.supply_ammo - 0.1)

    def night_atk(self, source, target_fleet):
        if not source.get_act_flag() or not source.get_act_indicator():
            return False

        act_flag = False
        atk_list = source.raise_night_atk(target_fleet)
        for atk in atk_list:
            act_flag = True
            hit_back = atk.start()  # 技能反击
            if isinstance(hit_back, ATK):
                hit_back.set_coef({'hit_back': True})
                hit_back.start()
        return act_flag
