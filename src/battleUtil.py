# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

from src.wsgr.wsgrTimer import Time
from src.wsgr.phase import *


class BattleUtil(Time):
    """调取全部战斗流程"""

    def __init__(self, friend, enemy):
        super().__init__()
        self.friend = friend
        self.enemy = enemy

    def battle_init(self):
        """战斗初始化"""
        self.timer.set_phase(AllPhase)
        for tmp_ship in self.friend.ship:
            tmp_ship.init_skill(self.friend, self.enemy)
            tmp_ship.init_health()
        for tmp_ship in self.enemy.ship:
            tmp_ship.init_skill(self.enemy, self.friend)
            tmp_ship.init_health()

    def battle_start(self):
        """进行阵型选择和战斗流程"""
        self.battle_init()
        self.recon_phase()
        self.get_direction()
        self.buff_phase()
        self.air_phase()

    def recon_phase(self):
        recon_flag = True  # 暂时默认索敌成功
        self.timer.set_recon(recon_flag=recon_flag)

    def get_direction(self):
        pass

    def buff_phase(self):
        self.timer.set_phase(BuffPhase(self.friend, self.enemy))
        self.timer.phase_start()

    def air_phase(self):
        self.timer.set_phase(AirPhase(self.friend, self.enemy))
        self.timer.phase_start()

    def end_phase(self):
        pass

    def report(self):
        pass


if __name__ == "__main__":
    pass
