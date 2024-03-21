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
        self.round_flag = None      # 迂回
        self.direction_flag = None  # 航向, 优同反劣分别为1-4
        self.air_con_flag = None    # 制空结果, 从空确到空丧分别为1-5
        self.phase = None           # 阶段
        self.atk = None
        self.env_skill = []         # 环境效果
        self.end_skill = []         # 结束阶段技能
        self.queue = {              # 有时点依赖的技能
            'magnet': [],           # 嘲讽
            'tank': [],             # 挡枪
            'chase': [],            # 追击
        }
        self.log = {
            'miss': np.zeros((len(damagePhaseList),2)),
            'hit': np.zeros((len(damagePhaseList),2)),
            'hit_rate': np.zeros((len(damagePhaseList),2)),
            'dcitem': 0,  # 使用损管数量
            'record': '',
            'create_damage': np.zeros((len(damagePhaseList),12)),
            'get_damage': np.zeros((len(damagePhaseList),12)),
            'defeat_num': np.zeros((len(damagePhaseList),12)),
            'damaged_state': np.zeros((len(damagePhaseList),12)),
            'supply': {'oil': 0, 'ammo': 0, 'steel': 0, 'almn': 0},
            # 'end_with': '',             # 退出时抵达位置
            # 'end_with_boss': False,     # 是否抵达boss点
        }

    def info(self, text: str):
        self.log['record'] += text

    def set_point(self, point):
        self.point = point
        if self.point.roundabout:
            rd = '/迂回'
        else:
            rd = ''
        self.info(f'-> {point}: {point.type.__name__}{rd}\n')

    def set_recon(self, recon_flag):
        self.recon_flag = recon_flag
        if recon_flag:
            self.info(f'索敌成功\n')
        else:
            self.info(f'索敌失败\n')

    def set_round(self, round_flag):
        self.round_flag = round_flag
        if round_flag:
            self.info(f'迂回成功\n')
        else:
            self.info(f'迂回失败\n')

    def set_direction(self, direction_flag):
        self.direction_flag = direction_flag
        direction_info = ['T优', '同航', '反航', 'T劣']
        self.info(f"我方航向：{direction_info[direction_flag - 1]}\n")

    def set_air_con(self, air_con_flag):
        self.air_con_flag = air_con_flag
        air_con_info = ['空确', '空优', '均势', '劣势', '丧失']
        self.info(f"制空结果：{air_con_info[air_con_flag - 1]}\n")

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

    def run_end_skill(self, friend, enemy):
        """结算结束阶段技能"""
        for tmp_skill in self.end_skill:
            tmp_skill.activate(friend, enemy)

    def get_dist(self):
        if self.point is not None:
            return self.point.level
        else:
            return 5  # 特殊点位手动置为5

    def get_dist_from_start(self):
        if self.point is not None:
            return 6 - self.point.level
        else:
            return 5  # 特殊点位手动置为5

    def queue_append(self, buff):
        if buff.name == 'chase':
            self.queue['chase'].append(buff)
            self.queue['chase'].sort(key=lambda x: x.master.loc)
        else:
            if buff.name == 'tank':
                queue = self.queue['tank']
            else:  # magnet & un_magnet
                queue = self.queue['magnet']
            queue.append(buff)
            queue.sort(key=lambda x: (-x.rate, x.master.loc))

    def reinit(self):
        """道中初始化timer状态，地图入口外每场战斗都要调用"""
        self.recon_flag = None      # 索敌
        self.direction_flag = None  # 航向
        self.round_flag = None      # 迂回
        self.air_con_flag = None    # 制空结果
        self.atk = None
        self.log.update({
            'miss': np.zeros((len(damagePhaseList),2)),
            'hit': np.zeros((len(damagePhaseList),2)),
            'hit_rate': np.zeros((len(damagePhaseList),2)),
            'result': '',
            'create_damage': np.zeros((len(damagePhaseList),12)),
            'get_damage': np.zeros((len(damagePhaseList),12)),
            'defeat_num': np.zeros((len(damagePhaseList),12)),
            'damaged_state': np.zeros((len(damagePhaseList),12)),
        })
        for key in self.queue.keys():
            self.queue.update({key: []})

    def phase_start(self):
        self.phase.start()

    def report_log(self, key, item):
        self.log[key] = item

    def report_result(self, result):
        self.log['result'] = result

    def report_damage(self, damage_value, sink):
        """伤害细节报告"""
        self.log['record'] += f"{type(self.atk).__name__}: " \
                              f"{self.atk.atk_body.status['name']} -> " \
                              f"{self.atk.target.status['name']}: " \
                              f"{str(damage_value)}\n"

        # 命中/闪避报告
        phase = type(self.phase).__name__
        phaseId = damagePhaseList.index(phase)
        if phase != 'SupportPhase':
            if isinstance(damage_value, str):
                self.log['miss'][phaseId, self.atk.atk_body.side] += 1
            else:
                self.log['hit'][phaseId, self.atk.atk_body.side] += 1

        # 伤害报告
        if not isinstance(damage_value, str):
            self.atk.atk_body.create_damage(damage_value)
            if sink:
                self.atk.atk_body.defeat_enemy()

    def phase_end_report(self, friend, enemy):
        """一个伤害阶段结束后统计战斗伤害信息"""
        phase = type(self.phase).__name__
        phaseId = damagePhaseList.index(phase)

        # 造成的伤害
        self.log['create_damage'][phaseId, :len(friend.ship)] = np.array(
            [ship.created_damage.get(phase, 0.) for ship in friend.ship])
        self.log['create_damage'][phaseId, 6:6+len(enemy.ship)] = np.array(
            [ship.created_damage.get(phase, 0.) for ship in enemy.ship])

        # 受到的伤害(到当前阶段的总和)
        self.log['get_damage'][phaseId, :len(friend.ship)] = np.array(
            [ship.got_damage for ship in friend.ship])
        self.log['get_damage'][phaseId, 6:6+len(enemy.ship)] = np.array(
            [ship.got_damage for ship in enemy.ship])

        # 击沉敌舰数目
        self.log['defeat_num'][phaseId, :len(friend.ship)] = np.array(
            [ship.defeated_enemy.get(phase, 0.) for ship in friend.ship])
        self.log['defeat_num'][phaseId, 6:6+len(enemy.ship)] = np.array(
            [ship.defeated_enemy.get(phase, 0.) for ship in enemy.ship])

        # 破损状态
        self.log['damaged_state'][phaseId, :len(friend.ship)] = np.array(
            [ship.damaged for ship in friend.ship])
        self.log['damaged_state'][phaseId, 6:6+len(enemy.ship)] = np.array(
            [ship.damaged for ship in enemy.ship])

        # 命中率
        hit_num = float(self.log['hit'][phaseId, 1])
        miss_num = float(self.log['miss'][phaseId, 1])
        try:
            self.log['hit_rate'][phaseId, 1] = (hit_num / (hit_num + miss_num))
        except:
            self.log['hit_rate'][phaseId, 1] = 0.
        hit_num = float(self.log['hit'][phaseId, 0])
        miss_num = float(self.log['miss'][phaseId, 0])
        try:
            self.log['hit_rate'][phaseId, 0] = (hit_num / (hit_num + miss_num))
        except:
            self.log['hit_rate'][phaseId, 0] = 0.


class Time:
    def __init__(self, timer):
        self.timer = timer

    def set_timer(self, new_timer):
        self.timer = new_timer


damagePhaseList = ['LongMissilePhase',
                   'SupportPhase',
                   'AirPhase',
                   'FirstMissilePhase',
                   'AntiSubPhase',
                   'FirstTorpedoPhase',
                   'FirstShellingPhase',
                   'SecondShellingPhase',
                   'SecondTorpedoPhase',
                   'SecondMissilePhase',
                   'NightPhase']
