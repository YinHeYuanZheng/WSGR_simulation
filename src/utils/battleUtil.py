# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import numpy as np
from src.wsgr.wsgrTimer import Time, damagePhaseList
from src.wsgr.phase import *

__all__ = ['BattleUtil',
           'Entrance',
           'MidPoint',
           'NormalBattle',
           'AirBattle',
           'NightBattle',
           'DaytimeBattle',
           'OnlyAirBattle',
           'SpecialBattle']


class BattleUtil(Time):
    """调取全部战斗流程"""

    def __init__(self, timer, friend, enemy):
        super().__init__(timer)
        self.friend = friend
        self.enemy = enemy
        self.start_health = None

    def start(self):
        """进行战斗流程"""
        self.battle_init()
        self.start_phase()
        self.run_phase(LongMissilePhase)
        self.run_phase(BuffPhase)
        # self.run_phase(SupportPhase)
        self.run_phase(AirPhase)
        self.run_phase(TLockPhase)
        self.run_phase(FirstMissilePhase)
        self.run_phase(AntiSubPhase)
        self.run_phase(FirstTorpedoPhase)
        self.run_phase(FirstShellingPhase)
        self.run_phase(SecondShellingPhase)
        self.run_phase(SecondTorpedoPhase)
        self.run_phase(SecondMissilePhase)
        self.run_phase(NightPhase)
        self.end_phase()

    def battle_init(self):
        """战斗初始化, 非地图入口时返回reinit"""
        if self.timer.point is not None and self.timer.point.level != 0:
            return self.battle_reinit()

        self.timer.set_phase(AllPhase(self.timer, self.friend, self.enemy))

        # 环境buff
        from src.utils.envBuffUtil import env
        for skill in env[:]:
            tmp_skill = skill(self.timer)
            self.timer.env_skill.append(tmp_skill)

        self.friend_init()
        self.enemy_init()

    def friend_init(self):
        # 初始化技能、耐久、补给
        for tmp_ship in self.friend.ship:
            tmp_ship.init_skill(self.friend, self.enemy)
            tmp_ship.init_health()
            tmp_ship.init_supply()

        # 计算索敌、航速相关舰队属性(只用于带路判断)
        self.friend.get_init_status(enemy=self.enemy)

    def enemy_init(self):
        # 初始化技能
        for tmp_ship in self.enemy.ship:
            tmp_ship.init_skill(self.enemy, self.friend)
            tmp_ship.init_health()

        # 计算索敌、航速相关舰队属性(只用于带路判断)
        self.enemy.get_init_status(enemy=self.friend)

    def battle_reinit(self):
        """道中初始化舰船状态，地图入口外每场战斗都要调用"""
        self.timer.set_phase(AllPhase(self.timer, self.friend, self.enemy))
        for tmp_ship in self.friend.ship:
            tmp_ship.reinit()
        self.enemy_init()
        self.timer.reinit()

    def start_phase(self):
        self.start_health = {
            1: np.sum([ship.status['health'] for ship in self.friend.ship]),
            0: np.sum([ship.status['health'] for ship in self.enemy.ship])
        }
        self.run_phase(PreparePhase)

    def run_phase(self, phase_class):
        """
        运行指定阶段
        :param phase_class: class src.wsgr.phase.AllPhase
        """
        self.timer.set_phase(phase_class(self.timer, self.friend, self.enemy))
        self.timer.phase_start()
        if phase_class.__name__ in damagePhaseList:
            self.timer.phase_end_report(self.friend, self.enemy)

    def supply_cost(self):
        """扣除昼战消耗，夜战在NightPhase内扣除"""
        for tmp_ship in self.friend.ship:
            tmp_ship.supply_oil = max(0, tmp_ship.supply_oil - 2)
            tmp_ship.supply_ammo = max(0, tmp_ship.supply_ammo - 2)

    def end_phase(self):
        # 结束阶段技能
        self.timer.run_end_skill(self.friend, self.enemy)

        # 资源消耗
        if not self.timer.round_flag:
            self.supply_cost()

        # 受伤记录
        end_health = {
            1: np.sum([ship.status['health'] for ship in self.friend.ship]),
            0: np.sum([ship.status['health'] for ship in self.enemy.ship])
        }

        # 战果条，视角符合游戏结算时战果条左右关系
        damage_progress = {
            1: 1 - end_health[0] / self.start_health[0],
            0: 1 - end_health[1] / self.start_health[1]
        }

        # 被击沉数量
        enemy_retreat_num = 0
        for tmp_ship in self.enemy.ship:
            if tmp_ship.damaged == 4:
                enemy_retreat_num += 1

        # 敌方全部被击沉
        if damage_progress[1] == 1:
            if damage_progress[0] == 0:
                self.timer.report_result('SS')
            else:
                self.timer.report_result('S')

        # 敌方旗舰被击沉
        elif self.enemy.ship[0].damaged == 4:
            if damage_progress[0] == 0:
                self.timer.report_result('A')
            else:
                self.timer.report_result('B')

        # 敌方被击沉超过2/3
        elif enemy_retreat_num >= len(self.enemy.ship) * 2/3:
            self.timer.report_result('A')

        # 敌方被击沉小于2/3，但战损比超过3倍，且我方战果条大于等于21%
        elif enemy_retreat_num < len(self.enemy.ship) * 2/3 and \
                damage_progress[1] >= damage_progress[0] * 3 and \
                damage_progress[1] >= 0.21:
            self.timer.report_result('B')

        # 我方未造成任何伤害，或战损比小于1/3
        elif damage_progress[1] == 0 or \
                damage_progress[1] * 3 < damage_progress[0]:
            self.timer.report_result('D')

        # 我方击沉任意一艘非旗舰，且未受到伤害
        elif enemy_retreat_num > 0 and damage_progress[0] == 0:
            self.timer.report_result('B')

        # 我方未击沉任何船，且未受到伤害，且我方战果条大于等于21%
        elif enemy_retreat_num == 0 and damage_progress[0] == 0 and \
                damage_progress[1] >= 0.21:
            self.timer.report_result('B')

        else:
            self.timer.report_result('C')

    def report(self):
        # 消耗
        supply = self.timer.log['supply']
        for tmp_ship in self.friend.ship:
            ship_supply = tmp_ship.reset()
            supply['oil'] += int(ship_supply['oil'])
            supply['ammo'] += int(ship_supply['ammo'])
            supply['steel'] += int(ship_supply['steel'])
            supply['almn'] += int(ship_supply['almn'])
            supply['repeat'] += int(ship_supply['repeat'])
        self.timer.report_log('supply', supply)

        return self.timer.log


class Entrance(BattleUtil):
    """地图入口"""
    def start(self):
        self.battle_init()

    def enemy_init(self):
        pass


class NormalBattle(BattleUtil):
    """常规战斗点"""

    def start(self):
        """进行战斗流程"""
        self.battle_init()
        self.start_phase()
        if self.timer.round_flag:
            self.end_phase()
            return
        self.run_phase(LongMissilePhase)
        self.run_phase(BuffPhase)
        if (self.timer.point is not None) and (self.timer.point.level == 5):
            self.run_phase(SupportPhase)
        self.run_phase(AirPhase)
        self.run_phase(TLockPhase)
        self.run_phase(FirstMissilePhase)
        self.run_phase(AntiSubPhase)
        self.run_phase(FirstTorpedoPhase)
        self.run_phase(FirstShellingPhase)
        self.run_phase(SecondShellingPhase)
        self.run_phase(SecondTorpedoPhase)
        self.run_phase(SecondMissilePhase)
        if (self.timer.point is None) or (self.timer.point.level == 5):
            self.run_phase(NightPhase)
        self.end_phase()


class AirBattle(BattleUtil):
    """航空战点"""

    def start(self):
        """进行战斗流程"""
        self.battle_init()
        self.start_phase()
        if self.timer.round_flag:
            self.end_phase()
            return
        self.run_phase(LongMissilePhase)
        self.run_phase(BuffPhase)
        self.run_phase(AirPhase)
        self.run_phase(TLockPhase)
        if (self.timer.point is None) or (self.timer.point.level == 5):
            self.run_phase(NightPhase)
        self.end_phase()

    def supply_cost(self):
        for tmp_ship in self.friend.ship:
            tmp_ship.supply_oil = max(0, tmp_ship.supply_oil - 1)
            tmp_ship.supply_ammo = max(0, tmp_ship.supply_ammo - 1)


class NightBattle(BattleUtil):
    """夜战点"""

    def start(self):
        """进行战斗流程"""
        self.battle_init()
        self.start_phase()
        if self.timer.round_flag:
            self.end_phase()
            return
        self.run_phase(LongMissilePhase)
        self.run_phase(BuffPhase)
        self.run_phase(TLockPhase)
        self.run_phase(NightPhase)
        self.end_phase()

    def supply_cost(self):
        pass


class MidPoint(BattleUtil):
    """无战斗点"""
    def start(self):
        pass

    def enemy_init(self):
        pass


# ## 以下为gui配套 ## #
class DaytimeBattle(BattleUtil):
    """无夜战"""
    def start(self):
        self.battle_init()
        self.start_phase()
        self.run_phase(LongMissilePhase)
        self.run_phase(BuffPhase)
        self.run_phase(AirPhase)
        self.run_phase(TLockPhase)
        self.run_phase(FirstMissilePhase)
        self.run_phase(AntiSubPhase)
        self.run_phase(FirstTorpedoPhase)
        self.run_phase(FirstShellingPhase)
        self.run_phase(SecondShellingPhase)
        self.run_phase(SecondTorpedoPhase)
        self.run_phase(SecondMissilePhase)
        self.end_phase()

class OnlyAirBattle(BattleUtil):
    """仅航空战"""
    def start(self):
        """进行战斗流程"""
        self.battle_init()
        self.start_phase()
        self.run_phase(BuffPhase)
        self.run_phase(AirPhase)
        self.end_phase()


# ## 以下为自定义战斗 ## #
class SpecialBattle(BattleUtil):
    """自定义战斗流程"""
    def start(self, air_strike_num:int=4):
        self.battle_init()
        self.start_phase()
        self.run_phase(LongMissilePhase)
        self.run_phase(BuffPhase)
        self.air_strike(air_strike_num)  # 特殊航空开幕
        self.run_phase(TLockPhase)
        self.run_phase(FirstMissilePhase)
        self.run_phase(AntiSubPhase)
        self.run_phase(FirstTorpedoPhase)
        self.run_phase(FirstShellingPhase)
        self.run_phase(SecondShellingPhase)
        self.run_phase(SecondTorpedoPhase)
        self.run_phase(SecondMissilePhase)
        self.run_phase(NightPhase)
        self.end_phase()

    def air_strike(self, air_strike_num:int):
        def get_form():
            return 4

        self.timer.set_phase(AirPhase(self.timer, self.friend, self.enemy))

        # 检查可被航空攻击的对象
        from src.wsgr.formulas import AirStrikeAtk
        def_friend = self.friend.get_atk_target(atk_type=AirStrikeAtk)
        # 如果不存在可攻击对象，结束本阶段
        if not len(def_friend):
            return

        # 创建深海攻击源
        from src.wsgr.ship import Ship
        supportUnit = Ship(self.timer)
        supportUnit.set_status(status={
            'name': '深海攻击',
            'accuracy': 120,
        })
        supportUnit.set_side(side := 0)
        supportUnit.set_load([20])
        supportUnit.get_form = get_form
        from src.wsgr.equipment import Bomber
        supportBomber = Bomber(self.timer, master=supportUnit, enum=0)
        supportBomber.set_status(status={
            'name':'深海高速轰炸机',
            'bomb': 10,
        })

        # 录入制空结果
        self.timer.report_log('aerial', [5, 0, 0])
        self.timer.set_air_con(5)

        # 结算攻击
        import src.wsgr.formulas as rform
        fall_coef, air_con_coef = rform.get_air_coef(self.timer.air_con_flag,
                                                     side)
        total_plane_rest = 20 * air_strike_num
        anti_num = [0] * len(def_friend)  # 迎击序数
        coef = {'actual_flight': 20,
                'air_con_fall': 0,
                'air_con_coef': air_con_coef}
        for i in range(air_strike_num):
            coef['anti_num'] = anti_num
            from src.wsgr.formulas import AirBombAtk
            atk = AirBombAtk(
                timer=self.timer,
                atk_body=supportUnit,
                def_list=def_friend,
                equip=supportBomber,
                coef=coef,
            )
            atk.start()
            anti_num = atk.get_coef('anti_num')


if __name__ == "__main__":
    pass
