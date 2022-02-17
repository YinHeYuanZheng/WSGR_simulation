# -*- coding: utf-8 -*-
# Author:银河远征
# env:py38
# 时统


class timer:
    """战斗时点依赖"""

    def __init__(self):
        self.recon_flag = None      # 索敌
        self.direction_flag = None  # 航向
        self.air_con_flag = None    # 制空结果
        self.phase = None           # 阶段
        self.queue = []             # 有时点依赖的技能 TODO 战斗结束记得清空

    def set_recon(self, recon_flag):
        self.recon_flag = recon_flag

    def set_direction(self, direction_flag):
        self.direction_flag = direction_flag

    def set_air_con(self, air_con_flag):
        self.air_con_flag = air_con_flag

    def set_phase(self, phase):
        self.phase = phase

    def phase_start(self):
        self.phase.start()


class Time:
    def __init__(self):
        self.timer = timer()

    def set_timer(self, new_timer):
        self.timer = new_timer
