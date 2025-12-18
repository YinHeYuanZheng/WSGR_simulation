# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import copy
import numpy as np
import threading
from src.wsgr.wsgrTimer import damagePhaseList
from src.wsgr.ship import Ship


def run_victory(battle, epoch,
                stop_event:threading.Event=None):
    result = [0] * 6
    result_flag_list = ['SS', 'S', 'A', 'B', 'C', 'D']
    for i in range(epoch):
        if stop_event is not None and stop_event.is_set():
            break
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        result_flag_id = result_flag_list.index(log['result'])
        result[result_flag_id] += 1
        print("\r"
              f"第{i + 1}次 - 战果分布: "
              f"SS {result[0] / (i + 1) * 100:.2f}% "
              f"S {result[1] / (i + 1) * 100:.2f}% "
              f"A {result[2] / (i + 1) * 100:.2f}% "
              f"B {result[3] / (i + 1) * 100:.2f}% "
              f"C {result[4] / (i + 1) * 100:.2f}% "
              f"D {result[5] / (i + 1) * 100:.2f}% ",
              end='',)


def run_map_victory(battle, epoch):
    result = [0] * 7
    result_flag_list = ['SS', 'S', 'A', 'B', 'C', 'D', '']
    for i in range(epoch):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()
        if log.get('end_with_boss'):
            result_flag_id = result_flag_list.index(log['result'])
            result[result_flag_id] += 1
        else:
            result[6] += 1
        print("\r"
              f"第{i + 1}次 - 战果分布: "
              f"SS {result[0] / (i + 1) * 100:.2f}% "
              f"S {result[1] / (i + 1) * 100:.2f}% "
              f"A {result[2] / (i + 1) * 100:.2f}% "
              f"B {result[3] / (i + 1) * 100:.2f}% "
              f"C {result[4] / (i + 1) * 100:.2f}% "
              f"D {result[5] / (i + 1) * 100:.2f}% "
              f"撤退 {result[6] / (i + 1) * 100:.2f}% ",
              end='',)


def run_hit_rate(battle, epoch, phase:str=None,
                 stop_event:threading.Event=None):
    hit_rate = 0
    for i in range(epoch):
        if stop_event is not None and stop_event.is_set():
            break
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        if (phase is not None) and (phase in damagePhaseList):
            phaseId = damagePhaseList.index(phase)
            hit_rate += log['hit_rate'][phaseId, 1]
        else:
            hit_rate += log['hit_rate'][:, 1].mean()
        print("\r"
              f"第{i + 1}次 - 命中率: {hit_rate / (i + 1) * 100: .4f}%",
              end='',)


def run_avg_damage(battle, epoch, phase:str=None,
                   stop_event:threading.Event=None):
    damage_list = np.zeros((epoch,), dtype=float)
    avg_damage_phase = 0
    defeat_num = 0
    for i in range(epoch):
        if stop_event is not None and stop_event.is_set():
            break
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        if (phase is not None) and (phase in damagePhaseList):
            phaseId = damagePhaseList.index(phase)
            avg_damage_phase += log['create_damage'][phaseId, :6].sum()
            phase_info = f'{phase}平均伤害: {avg_damage_phase / (i + 1):.3f} '
        else:
            phase_info = ''
        damage_list[i] = log['create_damage'][:, :6].sum()
        defeat_num += log['defeat_num'][:, :6].sum()
        print("\r"
              f"第{i + 1}次 - 平均伤害: {np.mean(damage_list[:i+1]):.3f} "
              f"5%下限伤害: {int(np.percentile(damage_list[:i+1], 5, method='lower')):d} "
              f"{phase_info}"
              f"平均击沉: {defeat_num / (i + 1):.3f}",
              end='',)


def run_supply_cost(battle, epoch,
                    stop_event:threading.Event=None):
    supply = {'oil': 0, 'ammo': 0, 'steel': 0, 'almn': 0, 'repeat': 0}
    for i in range(epoch):
        if stop_event is not None and stop_event.is_set():
            break
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        supply['oil'] += log['supply']['oil']
        supply['ammo'] += log['supply']['ammo']
        supply['steel'] += log['supply']['steel']
        supply['almn'] += log['supply']['almn']
        supply['repeat'] += log['supply']['repeat']
        print("\r"
              f"第{i + 1}次 - 资源消耗: "
              f"油 {supply['oil'] / (i + 1):.1f}, "
              f"弹 {supply['ammo'] / (i + 1):.1f}, "
              f"钢 {supply['steel'] / (i + 1):.1f}, "
              f"铝 {supply['almn'] / (i + 1):.1f},"
              f"桶 {supply['repeat'] / (i + 1):.2f}.",
              end='',)


def run_damaged(battle, epoch,
                stop_event:threading.Event=None):
    damaged_rate = np.zeros((6, 2))
    for i in range(epoch):
        if stop_event is not None and stop_event.is_set():
            break
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        for j in range(6):
            ship = tmp_battle.friend.ship[j]
            if ship.damaged >= 2:
                damaged_rate[j, 0] += 1
            if ship.damaged >= 3:
                damaged_rate[j, 1] += 1
        print("\r"
              f"第{i + 1}次 - "
              f"船名: "
              f"{tmp_battle.friend.ship[0].status['name']} "
              f"{tmp_battle.friend.ship[1].status['name']} "
              f"{tmp_battle.friend.ship[2].status['name']} "
              f"{tmp_battle.friend.ship[3].status['name']} "
              f"{tmp_battle.friend.ship[4].status['name']} "
              f"{tmp_battle.friend.ship[5].status['name']} "
              f"中破率: "
              f"{damaged_rate[0, 0] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[1, 0] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[2, 0] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[3, 0] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[4, 0] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[5, 0] / (i + 1) * 100:.2f}% "
              f"大破率: "
              f"{damaged_rate[0, 1] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[1, 1] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[2, 1] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[3, 1] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[4, 1] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[5, 1] / (i + 1) * 100:.2f}% "
              f"(注：中破率包含大破率)",
              end='',)


def new_hit_verify(value):
    """
    使用方法：
    ATK.outer_hit_verify = new_hit_verify(hit_rate)
    """
    def f(cls):
        if cls.atk_body.side == 1:  # 只修改深海命中
            return False
        if cls.target.size != 1:
            return False

        verify = np.random.random()
        if verify <= value:
            cls.coef['hit_flag'] = True
            return True
        else:
            cls.coef['hit_flag'] = False
            return True
    return f


def set_supply(battle, battle_num):
    """设置弹损，battle_num输入第几战"""
    for ship in battle.friend.ship:
        ship.supply_oil -= 2 * (battle_num - 1)
        ship.supply_ammo -= 2 * (battle_num - 1)


def change_shiptype(ship, ShipType:type(Ship)):
    ship.__class__ = ShipType


def prebattle_info(battle):
    tmp_battle = copy.deepcopy(battle)
    tmp_battle.start()
    log = tmp_battle.report()

    # 索敌
    recon_rate = log['recon'][0]
    friend_recon = log['recon'][1]
    recon_request = log['recon'][2]
    print(f"我方索敌-{friend_recon}  "
          f"索敌要求-{recon_request}  "
          f"索敌成功率：{recon_rate:d}%")

    # 制空
    air_con_flag = log['aerial'][0]
    aerial_friend = log['aerial'][1]
    aerial_enemy = log['aerial'][2]
    air_con_info = ['空确', '空优', '均势', '劣势', '丧失']
    if air_con_flag is not None:
        print(f"我方制空-{aerial_friend:.2f}  "
              f"敌方制空-{aerial_enemy:.2f}  "
              f"制空结果：{air_con_info[air_con_flag - 1]}")
    else:
        print("未进行航空战\n")


if __name__ == '__main__':
    pass
