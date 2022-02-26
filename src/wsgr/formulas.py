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
from .ship import AV

__all__ = ['ATK',
           'AirAtk',
           'AirBombAtk',
           'AirDiveAtk']


# attack types
class ATK(Time):
    """攻击总类"""

    def __init__(self, atk_body, def_list, coef, atk_form, def_form, changeable=True):
        super().__init__()
        self.timer.set_atk(self)
        self.atk_body = atk_body
        self.def_list = def_list  # 可被攻击目标列表
        self.target = None  # 攻击目标，可被更改
        self.coef = coef  # 伤害计算相关参数
        self.atk_form = atk_form  # 攻击方阵型
        self.def_form = def_form  # 防御方阵型

        self.form_coef = {
            'power': [],
            'hit': [],
            'miss': [],
            'crit': [],
            'be_crit': [],
        }  # 阵型系数
        self.changeable = changeable

    def start(self):
        """攻击开始命令，结算到攻击结束"""
        pass

    def set_target(self):
        # TODO 优先攻击分为随机和按顺序
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

    def get_form_coef(self, name, form_num):
        """获取阵型系数"""
        coef = self.form_coef.get(name)[form_num - 1]
        return coef

    def crit_verify(self):
        """暴击检定"""
        if self.get_coef('must_crit') or \
                self.atk_body.get_special_buff('must_crit', self):
            self.coef['crit'] = True
            return

        if self.get_coef('must_not_crit') or \
                self.target.get_special_buff('must_not_crit', self):
            self.coef['crit'] = False
            return

        # 基础暴击率
        crit = 0.05 + (self.atk_body.affection - 50) * 0.001 + \
               self.atk_body.get_atk_buff('crit', self) + \
               self.atk_body.get_final_status('luck') * 0.16 + \
               self.target.get_atk_buff('be_crit', self)

        # 阵型暴击率补正
        crit += self.get_form_coef('crit', self.atk_form) + \
                self.get_form_coef('be_crit', self.def_form)

        crit = cap(crit)
        verify = random.random()
        if verify < crit:
            self.coef['crit'] = True
            return
        else:
            self.coef['crit'] = False
            return

    def hit_verify(self):
        """命中检定"""
        if self.target.get_special_buff('shield', self):
            self.coef['hit'] = False
            return

        if self.get_coef('must_hit') or \
                self.atk_body.get_special_buff('must_hit', self):
            self.coef['hit'] = True
            return

        if self.get_coef('must_not_hit') or \
                self.target.get_special_buff('must_not_hit', self):
            self.coef['hit'] = False
            return

        accuracy = self.atk_body.get_final_status('accuracy')
        evasion = self.atk_body.get_final_status('evasion')
        if evasion == 0:
            evasion = 1
        hit_rate = accuracy / evasion / 2

    def get_dmg_coef(self):
        if self.atk_body.damaged == 1:
            return 1.
        elif self.atk_body.damaged == 2:
            return .6
        else:
            return .3

    def get_supply_coef(self):
        return min(1., self.atk_body.supply * 2)

    def formula(self):
        pass

    def final_damage(self, damage):
        for buff_scale in self.atk_body.get_final_damage_buff(self):
            damage = np.ceil(damage * (1 + buff_scale))
        for debuff_scale in self.target.get_final_damage_debuff(self):
            damage = np.ceil(damage * (1 + debuff_scale))
        # todo 可能会增加战术终伤
        return max(0, damage)

    def end_atk(self, damage_flag):
        """
        攻击结束时点，进行受伤时点效果、反击等
        :param damage_flag: 是否受到了伤害
        """
        if not damage_flag:
            return
        else:
            self.atk_body.atk_hit('atk_hit', self)
            self.target.atk_hit('be_atk_hit', self)


class AirAtk(ATK):
    def __init__(self, atk_body, def_list, equip, coef, atk_form, def_form, changeable=True):
        super().__init__(atk_body, def_list, coef, atk_form, def_form, changeable)
        self.equip = equip

        self.form_coef = {
            'power': [1, 1, 1, 1, 1],
            'hit': [1, 1, 1, 1, 1],
            'miss': [.8, 1., 1.2, .8, .9],
            'crit': [0, 0, 0, .25, 0],
            'be_crit': [0, 0, 0, .25, -.1],
            'anti_def': [1, 1.2, 1.6, 1, 1],
        }  # 阵型系数

    def start(self):
        damage_flag = False
        self.set_target()
        self.start_atk()

        self.hit_verify()  # 闪避检定
        self.crit_verify()  # 暴击检定
        self.process_coef()  # 生成公式相关系数

        if not self.coef['hit']:
            self.end_atk(damage_flag)
            return

        if self.coef['plane_rest'] == 0:
            self.end_atk(damage_flag)
            return

        damage = self.formula()
        if damage == 0:
            self.end_atk(damage_flag)
            return

        damage = self.final_damage(damage)
        damage_flag = self.target.get_damage(damage)
        self.end_atk(damage_flag)

    def get_anti_air_fall(self, anti_num):
        """计算防空击坠"""
        ignore_scale, ignore_bias = self.atk_body.get_atk_buff('ignore_antiair', self)  # 无视对空
        target_anti_air = self.target.get_final_status('anti_air', equip=False) * \
                          (1 + ignore_scale) + ignore_bias  # 本体裸对空
        target_anti_air = max(0, target_anti_air)

        team_anti_air = get_team_anti_air(self.def_list)  # 全队对空补正
        equip_anti_air = self.target.get_equip_status('anti_air')  # 装备对空总和
        aa_value = target_anti_air + team_anti_air + equip_anti_air
        aa_value *= self.get_form_coef('anti_def', self.def_form)  # todo 未明确

        alpha = random.random()
        bottom_a = 0.618
        aa_fall = np.floor(alpha * aa_value * bottom_a ** (anti_num - 1) / 10)
        return aa_fall

    def get_anti_air_def(self):
        """减伤对空"""
        ignore_scale, ignore_bias = self.atk_body.get_atk_buff('ignore_antiair', self)  # 无视对空
        target_anti_air = self.target.get_final_status('anti_air', equip=False) * \
                          (1 + ignore_scale) + ignore_bias  # 本体裸对空
        target_anti_air = max(0, target_anti_air)
        aa_value = target_anti_air + get_scaled_anti_air(self.target)
        return aa_value

    def hit_verify(self):
        """航空攻击命中检定，含对空预警，含飞机装备命中率buff"""
        # 护盾
        if self.target.get_special_buff('shield', self):
            self.coef['hit'] = False
            return

        # todo 对空预警

        # 技能必中
        if self.get_coef('must_hit') or \
                self.atk_body.get_special_buff('must_hit', self):
            self.coef['hit'] = True
            return

        # 技能必不中
        if self.get_coef('must_not_hit') or \
                self.target.get_special_buff('must_not_hit', self):
            self.coef['hit'] = False
            return

        # 基础命中率
        accuracy = self.atk_body.get_final_status('accuracy')
        evasion = self.atk_body.get_final_status('evasion')
        if evasion < 1:
            evasion = 1
        hit_rate = accuracy / evasion / 2

        # 阵型命中率补正
        hit_rate *= self.get_form_coef('hit', self.atk_form) / \
                    self.get_form_coef('miss', self.def_form)

        # 索敌补正
        if self.atk_body.side == 1 and self.timer.recon_flag:
            hit_rate += 0.05
        if self.target.side == 1 and self.timer.recon_flag:
            hit_rate += 0.05

        # 制空补正
        hit_rate += get_air_hit_coef(self.timer.air_con_flag,
                                     self.atk_body.side)

        # 船型补正
        aa_value = self.get_anti_air_def()
        if self.target.size == 3:
            aa_base = 1500
        elif self.target.size == 2:
            aa_base = 375
        else:
            aa_base = 150
        aa_hit_coef = aa_base / (aa_base + aa_value)
        hit_rate *= aa_hit_coef

        # 装备补正
        hit_rate += self.equip.get_atk_buff('hit_rate', self)

        # 技能补正
        hit_rate += self.atk_body.get_atk_buff('hit_rate', self)
        hit_rate -= self.target.get_atk_buff('miss_rate', self)

        hit_rate = cap(hit_rate)
        verify = random.random()
        if verify < hit_rate:
            self.coef['hit'] = True
            return
        else:
            self.coef['hit'] = False
            return

    def final_damage(self, damage):
        """航空战终伤"""

        # 额外伤害
        _, extra_damage = self.atk_body.get_atk_buff('extra_damage', self)
        damage += extra_damage

        # 终伤系数
        for buff_scale in self.atk_body.get_final_damage_buff(self):
            damage = np.ceil(damage * (1 + buff_scale))
        for debuff_scale in self.target.get_final_damage_debuff(self):
            damage = np.ceil(damage * (1 + debuff_scale))

        # 对空减伤
        aa_value = self.get_anti_air_def()
        if self.target.size == 3:
            aa_base = 150
        elif self.target.size == 2:
            aa_base = 375
        else:
            aa_base = 1500
        aa_damage_coef = aa_base / (aa_base + aa_value)
        damage = np.ceil(damage * aa_damage_coef)

        # todo 可能会增加战术终伤

        # 装母对轰炸减伤75%
        if isinstance(self.target, AV) and isinstance(self, AirBombAtk):
            damage = np.ceil(damage * .25)

        # 技能伤害减免
        _, reduce_damage = self.target.get_atk_buff('reduce_damage', self)
        damage -= reduce_damage

        return max(0, damage)


class AirBombAtk(AirAtk):
    def process_coef(self):
        target_num = self.get_target_num()
        self.coef['anti_num'][target_num] += 1
        anti_num = self.coef['anti_num'][target_num]
        aa_fall = self.get_anti_air_fall(anti_num)  # 防空击坠

        # 最大击坠量不超过实际放飞量
        actual_fall = min(self.coef['actual_flight'],
                          self.coef['air_con_fall'] + aa_fall)

        # 减少击坠技能
        fall_scale, fall_bias = self.atk_body.get_atk_buff('fall_rest', self)
        actual_fall = np.ceil(actual_fall * (1 + fall_scale) + fall_bias)
        actual_fall = max(0, actual_fall)  # 不会减到负数

        # 击坠结算与本次剩余载机量计算
        self.equip.fall(actual_fall)
        self.coef['plane_rest'] = self.coef['actual_flight'] - actual_fall

        # 技能系数
        skill_scale, _ = self.atk_body.get_atk_buff('air_atk_buff', self)
        self.coef['skill_coef'] = 1 + skill_scale
        skill_scale, _ = self.atk_body.get_atk_buff('air_bomb_atk_buff', self)
        self.coef['skill_coef'] *= (1 + skill_scale)

        # 船损系数
        self.coef['dmg_coef'] = self.get_dmg_coef()

        # 弹损系数
        self.coef['supply_coef'] = self.get_supply_coef()

        # 暴击系数
        if self.coef['crit']:
            _, crit_bias = self.atk_body.get_atk_buff('crit_coef', self)
            self.coef['crit_coef'] = 1.5 + crit_bias
        else:
            self.coef['crit_coef'] = 1.

        # 浮动系数
        self.coef['random_coef'] = random.uniform(.89, 1.22)

        # 穿甲系数
        _, pierce_bias = self.atk_body.get_atk_buff('pierce_coef', self)
        self.coef['pierce_coef'] = 0.6 + pierce_bias

        # 攻击者对系数进行最终修正（最高优先级）
        self.atk_body.atk_coef_process(self)

    def formula(self):
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
        ignore_scale, ignore_bias = self.atk_body.get_atk_buff('ignore_armor', self)  # 无视装甲
        def_armor = self.target.get_final_status('armor') * \
                    (1 + ignore_scale) + ignore_bias
        def_armor = max(0, def_armor)

        real_dmg = np.ceil(real_atk *
                           (1 - def_armor /
                            (0.5 * def_armor + self.coef['pierce_coef'] * real_atk)))

        if real_dmg <= 0:
            if np.random.random() < 0.5:  # 50% 跳弹
                return 0
            else:  # 50% 擦伤
                real_dmg = np.ceil(
                    min(real_atk, self.target.get_status('health')) * 0.1
                )
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

        # 减少击坠技能
        fall_scale, fall_bias = self.atk_body.get_atk_buff('fall_rest', self)
        actual_fall = np.ceil(actual_fall * (1 + fall_scale) + fall_bias)
        actual_fall = max(0, actual_fall)  # 不会减到负数

        # 击坠结算与本次剩余载机量计算
        self.equip.fall(actual_fall)
        self.coef['plane_rest'] = self.coef['actual_flight'] - actual_fall

        # 技能系数
        skill_scale, _ = self.atk_body.get_atk_buff('air_atk_buff', self)
        self.coef['skill_coef'] = 1 + skill_scale
        skill_scale, _ = self.atk_body.get_atk_buff('air_dive_atk_buff', self)
        self.coef['skill_coef'] *= (1 + skill_scale)

        # 船损系数
        self.coef['dmg_coef'] = self.get_dmg_coef()

        # 弹损系数
        self.coef['supply_coef'] = self.get_supply_coef()

        # 暴击系数
        if self.coef['crit']:
            _, crit_bias = self.atk_body.get_atk_buff('crit_coef', self)
            self.coef['crit_coef'] = 1.5 + crit_bias
        else:
            self.coef['crit_coef'] = 1.

        # 浮动系数
        self.coef['random_coef'] = random.uniform(.89, 1.22)

        # 鱼雷机系数
        self.coef['dive_random_coef'] = random.uniform(.5, 1.)

        # 穿甲系数
        _, pierce_bias = self.atk_body.get_atk_buff('pierce_coef', self)
        self.coef['pierce_coef'] = 2. + pierce_bias

        # 攻击者对系数进行最终修正（最高优先级）
        self.atk_body.atk_coef_process(self)

    def formula(self):
        # 基础攻击力
        base_status = self.equip.get_final_status('dive')
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
        ignore_scale, ignore_bias = self.atk_body.get_atk_buff('ignore_armor', self)
        def_armor = self.target.get_final_status('armor') * \
                    (1 + ignore_scale) + ignore_bias
        def_armor = max(0, def_armor)

        real_dmg = np.ceil(real_atk *
                           (1 - def_armor /
                            (0.5 * def_armor + self.coef['pierce_coef'] * real_atk)))

        if real_dmg <= 0:
            if np.random.random() < 0.5:  # 50% 跳弹
                return 0
            else:  # 50% 擦伤
                real_dmg = np.ceil(
                    min(real_atk, self.target.get_status('health')) * 0.1
                )
        return real_dmg


def cap(x):
    """将暴击率、命中率等锁定在5%-95%区间"""
    x = max(0.05, x)
    x = min(0.95, x)
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


def get_air_coef(air_con_flag, side):
    if side == 0:
        air_con_flag = 6 - air_con_flag

    if air_con_flag == 1:
        fall_coef = [0, 0.1]
        air_con_coef = 1.1
    elif air_con_flag == 2:
        fall_coef = [0.1, 0.3]
        air_con_coef = 1.05
    elif air_con_flag == 3:
        fall_coef = [0.3, 0.7]
        air_con_coef = 1.
    elif air_con_flag == 4:
        fall_coef = [0.7, 0.9]
        air_con_coef = .95
    else:
        fall_coef = [0.9, 1]
        air_con_coef = .9

    return fall_coef, air_con_coef


def get_air_hit_coef(air_con_flag, side):
    if side == 0:
        air_con_flag = 6 - air_con_flag

    if air_con_flag == 1:
        hit_rate = 0.1
    elif air_con_flag == 2:
        hit_rate = 0.05
    elif air_con_flag == 3:
        hit_rate = 0
    elif air_con_flag == 4:
        hit_rate = -0.05
    else:
        hit_rate = -0.1

    return hit_rate


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
                equip_aa_coef = tmp_equip.get_final_status('aa_coef')
                aa_coef = max(equip_aa_coef, aa_coef)
    return anti_air * aa_coef


def get_scaled_anti_air(ship):
    """获取(装备防空*防空倍率)之和"""
    anti_air = 0
    for tmp_equip in ship.equipment:
        equip_aa = tmp_equip.get_final_status('anti_air')
        equip_aa_scale = tmp_equip.get_final_status('anti_air_scale')
        anti_air += 2.5 * equip_aa * equip_aa_scale
    return anti_air


if __name__ == "__main__":
    pass
