# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import numpy as np
from src.wsgr.wsgrTimer import Time
from src.wsgr.phase import *


class BattleUtil(Time):
    """调取全部战斗流程"""

    def __init__(self, timer, friend, enemy):
        super().__init__(timer)
        self.friend = friend
        self.enemy = enemy

    def start(self):
        """进行战斗流程"""
        self.battle_init()
        self.start_phase()
        self.buff_phase()
        # self.air_phase()
        self.first_shelling_phase()
        # self.second_shelling_phase()
        self.end_phase()

    def battle_init(self):
        """战斗初始化, 只在第一场战斗进行调用"""
        self.timer.set_phase(AllPhase)
        for tmp_ship in self.friend.ship:
            tmp_ship.init_skill(self.friend, self.enemy)
            tmp_ship.init_health()
        for tmp_ship in self.enemy.ship:
            tmp_ship.init_skill(self.enemy, self.friend)
            tmp_ship.init_health()

        # 计算索敌、航速相关舰队属性(只用于带路判断)
        self.friend.get_init_status()
        self.enemy.get_init_status()

    def start_phase(self):
        self.timer.log['start_health'] = {
            1: np.array([ship.status['health'] for ship in self.friend.ship]),
            0: np.array([ship.status['health'] for ship in self.enemy.ship])
        }

        self.timer.set_phase(PreparePhase(self.timer, self.friend, self.enemy))
        self.timer.phase_start()

    def buff_phase(self):
        self.timer.set_phase(BuffPhase(self.timer, self.friend, self.enemy))
        self.timer.phase_start()

    def air_phase(self):
        self.timer.set_phase(AirPhase(self.timer, self.friend, self.enemy))
        self.timer.phase_start()

    def first_shelling_phase(self):
        self.timer.set_phase(FirstShellingPhase(self.timer, self.friend, self.enemy))
        self.timer.phase_start()

    def second_shelling_phase(self):
        self.timer.set_phase(SecondShellingPhase(self.timer, self.friend, self.enemy))
        self.timer.phase_start()

    def end_phase(self):
        # 大破进击取消保护
        for tmp_ship in self.friend.ship:
            if tmp_ship.damaged >= 3:
                tmp_ship.damage_protect = False

        # 清空buff
        self.friend.clear_buff()
        self.enemy.clear_buff()
        self.timer.reset_queue()

        # 受伤记录
        self.timer.log['end_health'] = {
            1: np.array([ship.status['health'] for ship in self.friend.ship]),
            0: np.array([ship.status['health'] for ship in self.enemy.ship])
        }
        self.timer.log['got_damage'] = {
            1: self.timer.log['start_health'][1] - self.timer.log['end_health'][1],
            0: self.timer.log['start_health'][0] - self.timer.log['end_health'][0]
        }

        # 战果条，视角符合游戏结算时战果条左右关系
        damage_progress = {
            1: np.sum(self.timer.log['got_damage'][0]) /
               np.sum(self.timer.log['start_health'][0]),
            0: np.sum(self.timer.log['got_damage'][1]) /
               np.sum(self.timer.log['start_health'][1])
        }

        # 被击沉数量
        enemy_retreat_num = 0
        for tmp_ship in self.enemy.ship:
            if tmp_ship.damaged == 4:
                enemy_retreat_num += 1
        self.timer.log['enemy_retreat_num'] = enemy_retreat_num

        # 敌方全部被击沉
        if damage_progress[1] == 1:
            if damage_progress[0] == 0:
                self.timer.log['result'] = 'SS'
            else:
                self.timer.log['result'] = 'S'

        # 敌方旗舰被击沉
        elif self.enemy.ship[0].damaged == 4:
            if damage_progress[0] == 0:
                self.timer.log['result'] = 'A'
            else:
                self.timer.log['result'] = 'B'

        # 敌方被击沉超过2/3
        elif enemy_retreat_num >= len(self.enemy.ship) * 2/3:
            self.timer.log['result'] = 'A'

        # 敌方被击沉小于2/3，但战损比超过3倍，且我方战果条大于等于21%
        elif enemy_retreat_num < len(self.enemy.ship) * 2/3 and \
                damage_progress[1] >= damage_progress[0] * 3 and \
                damage_progress[1] >= 0.21:
            self.timer.log['result'] = 'B'

        # 我方未造成任何伤害，或战损比小于1/3
        elif damage_progress[1] == 0 or \
                damage_progress[1] * 3 < damage_progress[0]:
            self.timer.log['result'] = 'D'

        # 我方击沉任意一艘非旗舰，且未受到伤害
        elif enemy_retreat_num > 0 and damage_progress[0] == 0:
            self.timer.log['result'] = 'B'

        # 我方未击沉任何船，且未受到伤害，且我方战果条大于等于21%
        elif enemy_retreat_num == 0 and damage_progress[0] == 0 and \
                damage_progress[1] >= 0.21:
            self.timer.log['result'] = 'B'

        else:
            self.timer.log['result'] = 'C'

    def report(self):
        try:
            hit_rate = self.timer.log['hit'] / \
                       (self.timer.log['hit'] + self.timer.log['miss'])
            self.timer.log['hit_rate'] = hit_rate
        except:
            self.timer.log['hit_rate'] = 0
        return self.timer.log


if __name__ == "__main__":
    pass
