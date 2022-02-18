# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 舰R公式

import numpy as np
import random
# import sys
# sys.path.append(r'.\wsgr')

from . import equipment as requip
from .wsgrTimer import Time

__all__ = ['ATK',
           'AirAtk',
           'AirBombAtk',
           'AirDiveAtk']


# attack types
class ATK(Time):
    """攻击总类"""

    def __init__(self, atk_body, def_list, coef, changeable=True):
        super().__init__()
        self.atk_body = atk_body
        self.def_list = def_list  # 可被攻击目标列表
        self.target = None  # 攻击目标，可被更改
        self.coef = coef  # 伤害计算相关参数

        self.changeable = changeable

    def start(self):
        """开始攻击，选定目标等"""
        pass

    def set_target(self):
        # TODO
        prior = self.atk_body.get_prior_target()
        if prior is not None:
            self.target = prior[0]
        else:
            self.target = random.choice(self.def_list)

    def get_target_num(self):
        # 遍历目标列表，查询目标所在位置
        for i in range(len(self.def_list)):
            if self.target == self.def_list[i]:
                return i

        # 遍历结束仍未查询到，报错
        raise AttributeError('target not in list!')

    def start_atk(self):
        """攻击开始时点，进行嘲讽判定等"""
        if not self.changeable:
            return
        if len(self.timer.queue):
            pass
            # for tmp_buff in self.timer.queue:
            #     if tmp_buff.is_active(self):
            #         tmp_buff.activate(self)

    def set_coef(self, name, value):
        self.coef[name] = value

    def process_coef(self):
        pass

    def get_coef(self, name):
        """获取指定名称的参数"""
        return self.coef.get(name, default=None)

    def crit_verify(self):
        """暴击检定"""
        if self.get_coef('must_crit'):
            return True

        crit = self.atk_body.get_final_status('crit') + \
               self.atk_body.get_final_status('luck') * 0.16
        crit = cap(crit)
        verify = random.random()
        if verify < crit:
            return True
        else:
            return False

    def hit_verify(self):
        """命中检定"""
        if self.get_coef('must_hit'):
            return True

        hit_rate = self.atk_body.get_final_status('accuracy') / \
                   self.atk_body.get_final_status('evasion') / 2

    def get_dmg_coef(self):
        if self.atk_body.damaged == 1:
            return 1.
        elif self.atk_body.get_special_buff('ignore_dmg'):
            return 1.
        elif self.atk_body.damaged == 2:
            return .6
        else:
            return .3

    def get_supply_coef(self):
        return min(1., self.atk_body.supply * 2)

    def formula(self):
        pass

    def damage(self, damage):
        damage = self.atk_body.give_damage(damage)
        self.target.get_damage(damage)

    def end_atk(self):
        """攻击结束时点，进行反击判定等"""
        pass


class AirAtk(ATK):
    def __init__(self, atk_body, def_list, equip, coef, changeable=True):
        super().__init__(atk_body, def_list, coef, changeable)
        self.equip = equip

        self.start()

    def start(self):
        self.set_target()
        self.start_atk()
        self.process_coef()
        damage = self.formula()
        if damage == 0:
            return
        self.damage(damage)
        self.end_atk()

    def get_anti_air_fall(self, anti_num):
        target_anti_air = self.target.get_final_status('anti_air', equip=False)  # 本体裸对空
        team_anti_air = get_team_anti_air(self.def_list)  # 全队对空补正
        aa_value = target_anti_air + team_anti_air
        alpha = random.random()
        bottom_a = 0.618
        aa_fall = np.floor(alpha * aa_value * bottom_a ** (anti_num - 1) / 10)
        return aa_fall

    def hit_verify(self):
        """TODO 航空攻击命中检定"""
        pass


class AirBombAtk(AirAtk):
    def process_coef(self):
        target_num = self.get_target_num()
        self.coef['anti_num'][target_num] += 1
        anti_num = self.coef['anti_num'][target_num]
        aa_fall = self.get_anti_air_fall(anti_num)  # 防空击坠

        # 最大击坠量不超过实际放飞量
        actual_fall = min(self.coef['actual_flight'],
                          self.coef['air_con_fall'] + aa_fall)

        # 击坠结算与本次剩余载机量计算
        self.equip.fall(actual_fall)
        self.coef['plane_rest'] = self.coef['actual_flight'] - actual_fall

        # 技能系数
        skill_scale, _ = self.atk_body.get_buff('air_atk_buff')
        self.coef['skill_coef'] = 1 + skill_scale
        skill_scale, _ = self.atk_body.get_buff('air_bomb_atk_buff')
        self.coef['skill_coef'] *= (1 + skill_scale)

        # 船损系数
        self.coef['dmg_coef'] = self.get_dmg_coef()

        # 弹损系数
        self.coef['supply_coef'] = self.get_supply_coef()

        # 暴击系数
        if self.crit_verify():
            self.coef['crit_coef'] = 1.5 + self.atk_body.get_buff('crit_coef')
        else:
            self.coef['crit_coef'] = 1.

        # 浮动系数
        self.coef['random_coef'] = random.uniform(.89, 1.22)

        # 穿甲系数
        pierce_scale, _ = self.atk_body.get_buff('pierce_coef')
        self.coef['pierce_coef'] = 0.6 + pierce_scale

        # TODO 对空预警

        # 闪避检定
        if self.hit_verify():
            self.coef['hit'] = True
        else:
            self.coef['hit'] = False

    def formula(self):
        if not self.coef['hit']:
            return 0
        if self.coef['plane_rest'] == 0:
            return 0

        # 基础攻击力
        base_status = self.equip.get_final_status('bomb')
        base_atk = 2 * np.log(self.coef['plane_rest'] + 1) * base_status + 25

        # 实际威力
        real_atk = (base_atk *
                    self.coef['skill_coef'] *
                    self.coef['air_con_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])

        # 实际伤害
        ignore_scale, ignore_bias = self.atk_body.get_buff('ignore_armor')  # 无视装甲
        def_armor = self.target.get_final_status('armor') * \
                    (1 + ignore_scale) + ignore_bias
        real_dmg = np.ceil(real_atk *
                           (1 - def_armor /
                            (0.5 * def_armor + self.coef['pierce_coef'] * real_atk)))
        return real_dmg


class AirDiveAtk(AirAtk):
    def process_coef(self):
        target_num = self.get_target_num()
        self.coef['anti_num'][target_num] += 1
        anti_num = self.coef['anti_num'][target_num]
        aa_fall = self.get_anti_air_fall(anti_num)  # 防空击坠

        # 最大击坠量不超过实际放飞量
        actual_fall = min(self.coef['actual_flight'],
                          self.coef['air_con_fall'] + aa_fall)

        # 击坠结算与本次剩余载机量计算
        self.equip.fall(actual_fall)
        self.coef['plane_rest'] = self.coef['actual_flight'] - actual_fall

        # 技能系数
        skill_scale, _ = self.atk_body.get_buff('air_atk_buff')
        self.coef['skill_coef'] = 1 + skill_scale
        skill_scale, _ = self.atk_body.get_buff('air_dive_atk_buff')
        self.coef['skill_coef'] *= (1 + skill_scale)

        # 船损系数
        self.coef['dmg_coef'] = self.get_dmg_coef()

        # 弹损系数
        self.coef['supply_coef'] = self.get_supply_coef()

        # 暴击系数
        if self.crit_verify():
            self.coef['crit_coef'] = 1.5 + self.atk_body.get_buff('crit_coef')
        else:
            self.coef['crit_coef'] = 1.

        # 浮动系数
        self.coef['random_coef'] = random.uniform(.89, 1.22)

        # 鱼雷机系数
        self.coef['dive_random_coef'] = random.uniform(.5, 1.)

        # 穿甲系数
        pierce_scale, _ = self.atk_body.get_buff('pierce_coef')
        self.coef['pierce_coef'] = 0.6 + pierce_scale

        # 闪避检定
        if self.hit_verify():
            self.coef['hit'] = True
        else:
            self.coef['hit'] = False

    def formula(self):
        if not self.coef['hit']:
            return 0
        if self.coef['plane_rest'] == 0:
            return 0

        # 基础攻击力
        base_status = self.equip.get_final_status('bomb')
        base_atk = 2 * np.log(self.coef['plane_rest'] + 1) * base_status + 25

        # 实际威力
        real_atk = (base_atk *
                    self.coef['skill_coef'] *
                    self.coef['air_con_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'] *
                    self.coef['dive_random_coef'])

        # 实际伤害
        ignore_scale, ignore_bias = self.atk_body.get_buff('ignore_armor')
        def_armor = self.target.get_final_status('armor') * \
                    (1 + ignore_scale) + ignore_bias
        real_dmg = np.ceil(real_atk *
                           (1 - def_armor /
                            (0.5 * def_armor + self.coef['pierce_coef'] * real_atk)))
        return real_dmg


def cap(x):
    """将暴击率、命中率等锁定在5%-95%区间"""
    if x < .05:
        x = .05
    elif x > .95:
        x = .95
    return x


def get_fleet_aerial(ship_list):
    """全队制空"""
    aerial = 0
    for tmp_ship in ship_list:
        aerial += get_ship_aerial(tmp_ship)
    return aerial


def get_ship_aerial(ship):
    """单船制空值"""
    flight_limit = get_flightlimit(ship)
    actual_flight = np.array([min(tmp_load, flight_limit)
                              for tmp_load in ship.load])
    antiair = np.array([tmp_equip.get_final_status('antiair')
                        for tmp_equip in ship.equipment])
    buff_scale, buff_bias = ship.get_buff('air_con_buff')

    air = np.log(2 * (actual_flight + 1)) * antiair
    result = np.sum(air) * (1 + buff_scale) + buff_bias

    return result


def compare_aerial(aerial_friend, aerial_enemy):
    """制空结果"""
    if aerial_friend >= aerial_enemy * 3:
        return 1  # 空确
    elif aerial_enemy * 3 > aerial_friend >= aerial_enemy * 3 / 2:
        return 2  # 优势
    elif aerial_enemy * 3 / 2 > aerial_friend >= aerial_enemy * 2 / 3:
        return 3  # 均势
    elif aerial_enemy * 2 / 3 > aerial_friend >= aerial_enemy * 1 / 3:
        return 4  # 劣势
    else:
        return 5  # 丧失


def get_total_plane_rest(shiplist):
    rest = 0
    for tmp_ship in shiplist:
        for tmp_equip in tmp_ship.equipment:
            if isinstance(tmp_equip, requip.Plane):
                rest += tmp_equip.load
    return rest


def get_flightlimit(ship):
    fire = max(ship.get_final_status('fire'), 0.)
    flightlimit = np.floor(fire / ship.flightparam) + 3
    return flightlimit


def get_air_con_fall(load, plane_rest, aerial, fall_rand):
    return np.floor((load / plane_rest) * aerial * fall_rand)


def get_team_anti_air(team):
    """获取全队补正防空"""
    anti_air = 0
    aa_coef = 0
    for tmp_ship in team:
        for tmp_equip in tmp_ship.equipment:
            if isinstance(tmp_equip, requip.AntiAirGun):
                anti_air += tmp_equip.get_final_status('anti_air')
                tmp_aa_coef = tmp_equip.get_final_status('aa_coef')
                if aa_coef < tmp_aa_coef:
                    aa_coef = tmp_aa_coef
    return anti_air * aa_coef


if __name__ == "__main__":
    pass
