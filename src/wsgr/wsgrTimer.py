# -*- coding: utf-8 -*-
# Author:银河远征
# env:py38
# 时统

import numpy as np


class timer:
    """战斗时点依赖"""

    def __init__(self):
        self.point = None           # 节点

        self.recon_flag = None      # 索敌
        self.direction_flag = None  # 航向, 优同反劣分别为1-4
        self.air_con_flag = None    # 制空结果, 从空确到空丧分别为1-5
        self.phase = None           # 阶段
        self.atk = None
        self.env_skill = []         # 环境效果
        self.queue = {              # 有时点依赖的技能
            'magnet': [],           # 嘲讽
            'tank': [],             # 挡枪
        }
        self.log = {
            'create_damage': {
                1: np.zeros((6,)),
                0: np.zeros((6,))
            },
            'miss': 0,
            'hit': 0,
            'record': '',
        }

    def set_point(self, point):
        self.point = point
        self.log['record'] += f'-> {point}: {point.type.__name__}\n'

    def set_recon(self, recon_flag):
        self.recon_flag = recon_flag

    def set_direction(self, direction_flag):
        self.direction_flag = direction_flag

    def set_air_con(self, air_con_flag):
        self.air_con_flag = air_con_flag
        air_con_info = ['空确', '空优', '均势', '劣势', '丧失']
        self.log['record'] += f"制空结果：{air_con_info[air_con_flag - 1]}\n"

    def set_phase(self, phase):
        self.phase = phase

    def set_atk(self, atk):
        self.atk = atk

    def run_prepare_skill(self, friend, enemy):
        """结算地图准备阶段技能"""
        for tmp_skill in self.env_skill:
            if tmp_skill.is_prep() and \
                    tmp_skill.is_active(friend, enemy):
                tmp_skill.activate(friend, enemy)

    def run_normal_skill(self, friend, enemy):
        """结算地图普通技能"""
        for tmp_skill in self.env_skill:
            if not tmp_skill.is_prep() and \
                    tmp_skill.is_active(friend, enemy):
                tmp_skill.activate(friend, enemy)

    def get_dist(self):
        # return self.point.level
        # 特殊点位手动置为5
        return 5

    def get_dist_from_start(self):
        # 特殊点位手动置为5
        return 5

    def queue_append(self, buff):
        if buff.name == 'tank':
            queue = self.queue['tank']
        else:
            queue = self.queue['magnet']

        queue.append(buff)
        queue.sort(key=lambda x: (-x.rate, x.master.loc))

    def reinit(self):
        self.recon_flag = None      # 索敌
        self.direction_flag = None  # 航向
        self.air_con_flag = None    # 制空结果
        self.atk = None
        self.log = {
            'create_damage': {
                1: np.zeros((6,)),
                0: np.zeros((6,))
            },
            'miss': 0,
            'hit': 0,
            'record': self.log['record']
        }
        self.queue = {
            'magnet': [],
            'tank': [],
        }

    def phase_start(self):
        self.phase.start()

    def report(self, damage_value):
        self.log['record'] += f"{type(self.atk).__name__}: " \
                              f"{self.atk.atk_body.status['name']} -> " \
                              f"{self.atk.target.status['name']}: " \
                              f"{str(damage_value)}\n"

        if self.atk.atk_body.side == 1:
            if isinstance(damage_value, str):
                self.log['miss'] += 1
            else:
                self.log['hit'] += 1
        if isinstance(damage_value, str):
            damage_value = 0
        self.log['create_damage'][self.atk.atk_body.side][self.atk.atk_body.loc - 1]\
            += damage_value


class Time:
    def __init__(self, timer):
        self.timer = timer

    def set_timer(self, new_timer):
        self.timer = new_timer
