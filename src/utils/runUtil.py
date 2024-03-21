# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import copy
import numpy as np
from src.wsgr.wsgrTimer import damagePhaseList


def run_victory(battle, epoc):
    result = [0] * 6
    result_flag_list = ['SS', 'S', 'A', 'B', 'C', 'D']
    for i in range(epoc):
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


def run_map_victory(battle, epoc):
    result = [0] * 7
    result_flag_list = ['SS', 'S', 'A', 'B', 'C', 'D', '']
    for i in range(epoc):
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


def run_hit_rate(battle, epoc, phase:str=None):
    hit_rate = 0
    for i in range(epoc):
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


def run_avg_damage(battle, epoc, phase:str=None):
    avg_damage = 0
    avg_damage_phase = 0
    defeat_num = 0
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        if (phase is not None) and (phase in damagePhaseList):
            phaseId = damagePhaseList.index(phase)
            avg_damage_phase += log['create_damage'][phaseId, :6].sum()
            phase_info = f'{phase}平均伤害: {avg_damage_phase / (i + 1):.3f} '
        else:
            phase_info = ''
        avg_damage += log['create_damage'][:, :6].sum()
        defeat_num += log['defeat_num'][:, :6].sum()
        print("\r"
              f"第{i + 1}次 - 平均伤害: {avg_damage / (i + 1):.3f} "
              f"{phase_info}"
              f"平均击沉 {defeat_num / (i + 1):.3f}",
              end='',)


def run_supply_cost(battle, epoc):
    supply = {'oil': 0, 'ammo': 0, 'steel': 0, 'almn': 0}
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        log = tmp_battle.report()

        supply['oil'] += log['supply']['oil']
        supply['ammo'] += log['supply']['ammo']
        supply['steel'] += log['supply']['steel']
        supply['almn'] += log['supply']['almn']
        print("\r"
              f"第{i + 1}次 - 资源消耗: "
              f"油 {supply['oil'] / (i + 1):.1f}, "
              f"弹 {supply['ammo'] / (i + 1):.1f}, "
              f"钢 {supply['steel'] / (i + 1):.1f}, "
              f"铝 {supply['almn'] / (i + 1):.1f}.",
              end='',)


def run_damaged(battle, epoc):
    damaged_rate = np.zeros((6, 2))
    for i in range(epoc):
        tmp_battle = copy.deepcopy(battle)
        tmp_battle.start()
        for j in range(6):
            ship = tmp_battle.friend.ship[j]
            if ship.damaged >= 2:
                damaged_rate[j, 0] += 1
            if ship.damaged >= 3:
                damaged_rate[j, 1] += 1
        print(f"第{i + 1}次 \n"
              f"船名 中破率 大破率\n"
              f"{tmp_battle.friend.ship[0].status['name']}   "
              f"{damaged_rate[0, 0] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[0, 1] / (i + 1) * 100:.2f}% \n"
              f"{tmp_battle.friend.ship[1].status['name']}   "
              f"{damaged_rate[1, 0] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[1, 1] / (i + 1) * 100:.2f}% \n"
              f"{tmp_battle.friend.ship[2].status['name']}   "
              f"{damaged_rate[2, 0] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[2, 1] / (i + 1) * 100:.2f}% \n"
              f"{tmp_battle.friend.ship[3].status['name']}   "
              f"{damaged_rate[3, 0] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[3, 1] / (i + 1) * 100:.2f}% \n"
              f"{tmp_battle.friend.ship[4].status['name']}   "
              f"{damaged_rate[4, 0] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[4, 1] / (i + 1) * 100:.2f}% \n"
              f"{tmp_battle.friend.ship[5].status['name']}   "
              f"{damaged_rate[5, 0] / (i + 1) * 100:.2f}% "
              f"{damaged_rate[5, 1] / (i + 1) * 100:.2f}%")


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


if __name__ == '__main__':
    pass
