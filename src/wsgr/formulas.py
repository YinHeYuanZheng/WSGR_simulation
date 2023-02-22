# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 舰R公式

import numpy as np

from src.wsgr.wsgrTimer import Time
from src.wsgr.equipment import *

__all__ = ['ATK',
           'SupportAtk',
           'AirAtk',
           'AirStrikeAtk',
           'AirBombAtk',
           'AirDiveAtk',
           'MissileAtk',
           'AntiSubAtk',
           'AirAntiSubAtk',
           'TorpedoAtk',
           'NormalAtk',
           'MagicAtk',
           'SpecialAtk',
           'AirNormalAtk',
           'NightAtk',
           'NightNormalAtk',
           'NightFirelAtk',
           'NightFireTorpedolAtk',
           'NightTorpedoAtk',
           'NightMissileAtk',
           'NightAntiSubAtk'
           ]


# attack types
class ATK(Time):
    """攻击总类"""

    def __init__(self, timer, atk_body, def_list, coef=None, target=None,
                 *args, **kwargs):
        super().__init__(timer)
        self.atk_body = atk_body
        self.def_list = def_list  # 可被攻击目标列表

        self.target = target  # 攻击目标，可被更改
        self.changeable = True  # 攻击目标是否可被更改

        if coef is None:
            coef = {}
        self.coef = coef  # 伤害计算相关参数

        self.form_coef = {
            'power': [],
            'hit': [],
            'miss': [],
            'crit': [0, 0, 0, .25, 0],
            'be_crit': [0, 0, 0, .25, -.1],
        }  # 阵型系数
        self.dir_coef = [1.15, 1., 0.8, 0.65]  # 航向系数，按照优同反劣顺序
        self.random_range = [0.89, 1.22]  # 浮动系数上下限
        self.pierce_base = 0.6  # 穿甲基础值

    def __repr__(self):
        source_name = self.atk_body.status['name']
        target_name = self.target.status['name'] \
            if self.target is not None else '未确定'
        return f"{source_name} -> {target_name} ({type(self).__name__})"

    def start(self):
        """攻击开始命令，结算到攻击结束"""
        self.timer.set_atk(self)
        damage_flag = False
        self.target_init()
        self.start_atk()

        self.hit_verify()  # 闪避检定
        self.crit_verify()  # 暴击检定
        self.process_coef()  # 生成公式相关系数

        if not self.coef['hit_flag']:
            return self.end_atk(damage_flag, 'miss')

        real_atk = self.formula()
        damage = self.real_damage(real_atk)
        if damage == 0:
            return self.end_atk(damage_flag, 'jump')

        damage_flag = True
        damage = self.final_damage(damage)
        damage = self.target.get_damage(damage)
        return self.end_atk(damage_flag, damage)

    def target_init(self):
        """决定攻击目标，技能可以影响优先目标"""
        if self.target is not None:
            return self.target

        # 优先站位攻击
        prior = self.atk_body.get_prior_loc_target(self.def_list)
        if prior is not None:
            assert not isinstance(prior, list)
            self.target = prior
            self.changeable = False
            return self.target
        else:
            self.target = np.random.choice(self.def_list)
            self.changeable = True

            # 嘲讽技能
            for tmp_buff in self.timer.queue['magnet']:
                if tmp_buff.is_active(self):
                    tmp_buff.activate(self)
                    break
            return self.target

    def set_target(self, target):
        self.target = target

    def start_atk(self):
        """攻击开始时点，进行挡枪判定、攻击时复杂效果结算等"""
        if len(self.timer.queue['tank']):
            for tmp_buff in self.timer.queue['tank']:
                if tmp_buff.is_active(self):
                    tmp_buff.activate(self)
                    break

        self.atk_body.atk_hit('give_atk', self)
        self.target.atk_hit('get_atk', self)

    def set_coef(self, coef):
        self.coef.update(coef)

    def process_coef(self):
        # 阵型系数
        self.coef['form_coef'] = self.get_form_coef('power', self.atk_body.get_form())

        # 技能系数
        skill_scale, _ = self.atk_body.get_atk_buff('power_buff', self)
        self.coef['skill_coef'] = 1 + skill_scale

        # 航向系数
        self.coef['dir_coef'] = self.get_dir_coef(self.atk_body.get_dir_flag())

        # 船损系数
        self.coef['dmg_coef'] = self.get_dmg_coef()

        # 弹损系数
        self.coef['supply_coef'] = self.get_supply_coef()

        # 暴击系数
        if self.coef['crit_flag']:
            _, crit_bias = self.atk_body.get_atk_buff('crit_coef', self)
            self.coef['crit_coef'] = 1.5 + crit_bias
        else:
            self.coef['crit_coef'] = 1.

        # 浮动系数
        if isinstance(self, NormalAtk):  # 炮击战普通炮击，结算超重弹
            _, equip_bias = self.atk_body.get_atk_buff('uplimit_buff', self)
        else:
            equip_bias = 0
        self.coef['random_coef'] = np.random.uniform(self.random_range[0],
                                                     self.random_range[1] + equip_bias)

        # 穿甲系数
        _, pierce_bias = self.atk_body.get_atk_buff('pierce_coef', self)
        self.coef['pierce_coef'] = self.pierce_base + pierce_bias

        # 攻击者对系数进行最终修正（最高优先级）
        self.atk_body.atk_coef_process(self)

    def get_coef(self, name):
        """获取指定名称的参数"""
        return self.coef.get(name, None)

    def get_coef_value(self, name):
        """获取指定名称的参数值"""
        return self.coef.get(name, 0)

    def get_form_coef(self, name, form_num):
        """获取阵型系数"""
        coef = self.form_coef.get(name)[form_num - 1]
        return coef

    def get_dir_coef(self, dir_num):
        return self.dir_coef[dir_num - 1]

    def crit_verify(self):
        """暴击检定"""
        if self.get_coef('must_crit') or \
                self.atk_body.get_special_buff('must_crit', self) or \
                self.target.get_special_buff('must_be_crit', self):
            self.coef['crit_flag'] = True
            return

        if self.get_coef('must_not_crit') or \
                self.atk_body.get_special_buff('must_not_crit', self) or \
                self.target.get_special_buff('must_not_be_crit', self):
            self.coef['crit_flag'] = False
            return

        # 基础暴击率
        crit = 0.05 + (self.atk_body.affection - 50) * 0.001 + \
               self.get_coef_value('crit') + \
               self.atk_body.get_atk_buff('crit', self)[1] + \
               self.atk_body.get_final_status('luck') * 0.0016 + \
               self.target.get_atk_buff('be_crit', self)[1]

        # 阵型暴击率补正
        crit += self.get_form_coef('crit', self.atk_body.get_form()) + \
                self.get_form_coef('be_crit', self.target.get_form())

        crit = cap(crit)
        verify = np.random.random()
        if verify <= crit:
            self.coef['crit_flag'] = True
            return
        else:
            self.coef['crit_flag'] = False
            return

    def hit_verify(self):
        """命中检定"""
        # 技能、战术判定
        if self.skill_hit_verify():
            return

        # 外部命中率修改
        if self.outer_hit_verify():
            return

        # 基础命中率
        accuracy = self.atk_body.get_final_status('accuracy')
        evasion = self.target.get_final_status('evasion')

        # 梯形锁定减少闪避
        if self.target.get_special_buff('t_lock'):
            evasion *= 0.9  # todo 数值未知

        hit_rate = accuracy / max(1, evasion) / 2

        # 阵型命中率补正
        hit_rate *= self.get_form_coef('hit', self.atk_body.get_form()) / \
                    self.get_form_coef('miss', self.target.get_form())

        # 索敌补正
        if self.atk_body.get_recon_flag():
            hit_rate *= 1.05
        if self.target.get_recon_flag():
            hit_rate *= 0.95

        # 船型补正
        d_size = self.atk_body.size - self.target.size
        hit_rate *= 1 - max(0, d_size * 0.1)

        # 单纵、复纵额外补正
        add = 0
        if self.target.get_form() == 2:
            add -= 0.05
        from src.wsgr.phase import SecondShellingPhase
        if self.atk_body.get_form() == 1 and \
                isinstance(self.timer.phase, SecondShellingPhase):
            add += 0.05
        hit_rate += add

        # 好感补正
        hit_rate += (self.atk_body.affection - 50) * 0.001
        hit_rate -= (self.target.affection - 50) * 0.001

        # 技能补正
        _, hitrate_bias = self.atk_body.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias
        _, hitrate_bias = self.target.get_atk_buff('miss_rate', self)
        hit_rate -= hitrate_bias

        hit_rate = cap(hit_rate)
        verify = np.random.random()
        if verify <= hit_rate:
            self.coef['hit_flag'] = True
            return
        else:
            self.coef['hit_flag'] = False
            return

    def skill_hit_verify(self):
        """必中/护盾等技能/战术判定"""
        # 护盾
        if self.target.get_special_buff('shield', self):
            self.coef['hit_flag'] = False
            return True

        # 大角度类战术
        if self.target.get_strategy_buff('strategy_shield', self):
            self.coef['hit_flag'] = False
            return True

        # 技能必中
        if self.get_coef('must_hit') or \
                self.get_coef('hit_back') or \
                self.atk_body.get_special_buff('must_hit', self):
            self.coef['hit_flag'] = True
            return True

        # 技能必不中
        if self.get_coef('must_not_hit') or \
                self.target.get_special_buff('must_not_hit', self):
            self.coef['hit_flag'] = False
            return True

        return False

    def outer_hit_verify(self):
        pass

    def get_dmg_coef(self):
        if self.get_coef('ignore_damaged'):
            return 1.
        elif self.atk_body.get_special_buff('ignore_damaged', self):
            return 1.
        elif self.atk_body.damaged == 1:
            return 1.
        elif self.atk_body.damaged == 2:
            return .6
        else:
            return .3

    def get_supply_coef(self):
        return min(1., self.atk_body.supply_ammo * 2)

    def formula(self):
        pass

    def real_damage(self, real_atk):
        if real_atk is None:
            raise ValueError(f'Formula of "{type(self).__name__}" is not defined!')

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
                    min(real_atk, self.target.status['health']) * 0.1
                )
        return real_dmg

    def final_damage(self, damage):
        """普通攻击终伤"""

        # 额外伤害
        _, extra_damage = self.atk_body.get_atk_buff('extra_damage', self)
        damage += extra_damage

        # 终伤增伤系数
        for buff_scale in self.atk_body.get_final_damage_buff(self):
            damage = np.ceil(damage * (1 + buff_scale))
        buff_scale = self.get_coef('final_damage_buff')
        if buff_scale:
            damage = np.ceil(damage * (1 + buff_scale))

        # 终伤减伤系数
        for debuff_scale in self.target.get_final_damage_debuff(self):
            damage = np.ceil(damage * (1 + debuff_scale))
        buff_scale = self.get_coef('final_damage_debuff')
        if buff_scale:
            damage = np.ceil(damage * (1 + buff_scale))

        # 挡枪减伤
        tank_damage_debuff = self.get_coef('tank_damage_debuff')
        if tank_damage_debuff is not None:
            damage = np.ceil(damage * (1 + tank_damage_debuff))

        # 战术终伤
        buff_scale = self.atk_body.get_strategy_value('final_damage_buff', self)
        if buff_scale:
            damage = np.ceil(damage * (1 + buff_scale))
        debuff_scale = self.target.get_strategy_value('final_damage_debuff', self)
        if debuff_scale:
            damage = np.ceil(damage * (1 + debuff_scale))

        # 技能伤害减免
        _, reduce_damage = self.target.get_atk_buff(name='reduce_damage',
                                                    atk=self,
                                                    damage=damage)
        damage -= reduce_damage

        return max(0, damage)

    def end_atk(self, damage_flag, damage_value):
        """
        攻击结束时点，进行受伤时点效果、反击等
        :param damage_flag: 是否受到了伤害
        :param damage_value: 伤害记录
        """
        hit_back = None
        chase_atk = None
        if not damage_flag:
            self.timer.report('miss')
        else:
            self.atk_body.atk_hit('atk_hit', self)
            hit_back = self.target.atk_hit('atk_be_hit', self)
            for tmp_buff in self.timer.queue['chase']:
                if tmp_buff.is_active(self):
                    chase_atk = tmp_buff.activate(self)
                    break
            self.timer.report(damage_value)

        self.atk_body.remove_during_buff()
        self.target.remove_during_buff()
        return hit_back, chase_atk


class SupportAtk(ATK):
    """支援攻击"""

    def start(self):
        self.timer.set_atk(self)
        damage = self.formula()
        damage_flag = bool(damage)
        damage = self.target.get_damage(damage)
        return self.end_atk(damage_flag, damage)

    def formula(self):
        damage = np.random.uniform(60, 100)
        return np.ceil(damage)

    def end_atk(self, damage_flag, damage_value):
        hit_back = None
        chase_atk = None
        if not damage_flag:
            self.timer.report('miss')
        else:
            self.timer.report(damage_value)
        return hit_back, chase_atk


class AirAtk(ATK):
    """航空攻击，包含航空战AirStrikeAtk、炮击战AirNormalAtk、炮击战航空反潜AirAntiSubAtk"""
    def __init__(self, timer, atk_body, def_list, coef=None, target=None):
        super().__init__(timer, atk_body, def_list, coef, target)
        self.equip = None

    def get_anti_air_def(self):
        """减伤对空"""
        ignore_scale, ignore_bias = self.atk_body.get_atk_buff('ignore_antiair', self)  # 无视对空
        target_anti_air = self.target.get_final_status('antiair', equip=False) * \
                          (1 + ignore_scale) + ignore_bias  # 本体裸对空
        target_anti_air = max(0, target_anti_air)
        aa_value = target_anti_air + get_scaled_anti_air(self.target)
        return aa_value


class AirStrikeAtk(AirAtk):
    """航空战航空攻击"""
    def __init__(self, timer, atk_body, def_list, equip, coef,
                 target=None):
        super().__init__(timer, atk_body, def_list, coef, target)
        self.equip = equip

        self.form_coef.update({
            'power': [1, 1, 1, 1, 1],
            'hit': [1, 1, 1, 1, 1],
            'miss': [.8, 1., 1.2, .8, .9],
            'anti_def': [1, 1.2, 1.6, 1, 1],
        })  # 阵型系数

    def start(self):
        self.timer.set_atk(self)
        damage_flag = False
        self.target_init()
        self.start_atk()

        self.hit_verify()  # 闪避检定
        self.crit_verify()  # 暴击检定
        self.process_coef()  # 生成公式相关系数

        if not self.coef['hit_flag']:
            return self.end_atk(damage_flag, 'miss')

        if self.coef['plane_rest'] == 0:
            return self.end_atk(damage_flag, 'miss')

        real_atk = self.formula()
        damage = self.real_damage(real_atk)
        if damage == 0:
            return self.end_atk(damage_flag, 'jump')

        damage_flag = True
        damage = self.final_damage(damage)
        damage = self.target.get_damage(damage)
        return self.end_atk(damage_flag, damage)

    def get_anti_air_fall(self, anti_num):
        """计算防空击坠"""
        ignore_scale, ignore_bias = self.atk_body.get_atk_buff('ignore_antiair', self)  # 无视对空
        target_anti_air = self.target.get_final_status('antiair', equip=False) * \
                          (1 + ignore_scale) + ignore_bias  # 本体裸对空
        target_anti_air = max(0, target_anti_air)

        team_anti_air = get_team_anti_air(self.def_list)  # 全队对空补正
        equip_anti_air = self.target.get_equip_status('antiair')  # 装备对空总和
        aa_value = target_anti_air + team_anti_air + equip_anti_air
        if self.target.function == 'cover':
            aa_value *= self.get_form_coef('anti_def', self.target.get_form())  # todo 未明确

        alpha = np.random.random()
        bottom_a = 0.618
        aa_fall = np.floor(alpha * aa_value * bottom_a ** (anti_num - 1) / 10)
        return aa_fall

    def hit_verify(self):
        """航空攻击命中检定，含飞机装备命中率buff"""
        # 技能、战术判定
        if self.skill_hit_verify():
            return

        # 外部命中率修改
        if self.outer_hit_verify():
            return

        # 基础命中率
        accuracy = self.atk_body.get_final_status('accuracy')

        hit_rate = accuracy / 50 / 2
        hit_rate = min(1, hit_rate)

        # 阵型命中率补正
        hit_rate *= self.get_form_coef('hit', self.atk_body.get_form()) / \
                    self.get_form_coef('miss', self.target.get_form())

        # 索敌补正
        if self.atk_body.get_recon_flag():
            hit_rate *= 1.05
        if self.target.get_recon_flag():
            hit_rate *= 0.95

        # 制空补正
        hit_rate *= 1 + get_air_hit_coef(self.atk_body.get_air_con_flag())

        # 船型补正
        aa_value = self.get_anti_air_def()
        if self.target.size == 3:
            aa_base = 1500
            mul_rate = 1
        elif self.target.size == 2:
            aa_base = 375
            mul_rate = 0.75
        else:
            aa_base = 150
            mul_rate = 0.5
        aa_hit_coef = aa_base / (aa_base + aa_value)
        hit_rate *= aa_hit_coef * mul_rate

        # 装备补正
        _, hitrate_bias = self.equip.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias

        # 好感补正
        hit_rate += (self.atk_body.affection - 50) * 0.001
        hit_rate -= (self.target.affection - 50) * 0.001

        # 技能补正
        _, hitrate_bias = self.atk_body.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias
        _, hitrate_bias = self.target.get_atk_buff('miss_rate', self)
        hit_rate -= hitrate_bias

        hit_rate = cap(hit_rate)
        verify = np.random.random()
        if verify <= hit_rate:
            self.coef['hit_flag'] = True
            return
        else:
            self.coef['hit_flag'] = False
            return

    def final_damage(self, damage):
        """航空攻击终伤"""

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

        # 装母对轰炸减伤75%
        from src.wsgr.ship import AV
        if isinstance(self.target, AV) and isinstance(self, AirBombAtk):
            damage = np.ceil(damage * .25)

        # 额外伤害
        _, extra_damage = self.atk_body.get_atk_buff('extra_damage', self)
        damage += extra_damage

        # 终伤增伤系数
        for buff_scale in self.atk_body.get_final_damage_buff(self):
            damage = np.ceil(damage * (1 + buff_scale))
        buff_scale = self.get_coef('final_damage_buff')
        if buff_scale:
            damage = np.ceil(damage * (1 + buff_scale))

        # 终伤减伤系数
        for debuff_scale in self.target.get_final_damage_debuff(self):
            damage = np.ceil(damage * (1 + debuff_scale))
        buff_scale = self.get_coef('final_damage_debuff')
        if buff_scale:
            damage = np.ceil(damage * (1 + buff_scale))

        # 战术终伤
        buff_scale = self.atk_body.get_strategy_value('final_damage_buff', self)
        if buff_scale:
            damage = np.ceil(damage * (1 + buff_scale))
        debuff_scale = self.target.get_strategy_value('final_damage_debuff', self)
        if debuff_scale:
            damage = np.ceil(damage * (1 + debuff_scale))

        # 技能伤害减免
        _, reduce_damage = self.target.get_atk_buff(name='reduce_damage',
                                                    atk=self,
                                                    damage=damage)
        damage -= reduce_damage

        return max(0, damage)


class AirBombAtk(AirStrikeAtk):
    def process_coef(self):
        target_num = self.def_list.index(self.target)
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
        if self.coef['crit_flag']:
            _, crit_bias = self.atk_body.get_atk_buff('crit_coef', self)
            self.coef['crit_coef'] = 1.5 + crit_bias
        else:
            self.coef['crit_coef'] = 1.

        # 浮动系数
        self.coef['random_coef'] = np.random.uniform(self.random_range[0],
                                                     self.random_range[1])

        # 穿甲系数
        _, pierce_bias = self.atk_body.get_atk_buff('pierce_coef', self)
        self.coef['pierce_coef'] = 1. + pierce_bias

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
        return real_atk


class AirDiveAtk(AirStrikeAtk):
    def process_coef(self):
        target_num = self.def_list.index(self.target)
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
        if self.coef['crit_flag']:
            _, crit_bias = self.atk_body.get_atk_buff('crit_coef', self)
            self.coef['crit_coef'] = 1.5 + crit_bias
        else:
            self.coef['crit_coef'] = 1.

        # 浮动系数
        self.coef['random_coef'] = np.random.uniform(self.random_range[0],
                                                     self.random_range[1])

        # 鱼雷机系数
        self.coef['dive_random_coef'] = np.random.uniform(.5, 1.)

        # 穿甲系数
        _, pierce_bias = self.atk_body.get_atk_buff('pierce_coef', self)
        self.coef['pierce_coef'] = 2. + pierce_bias

        # 攻击者对系数进行最终修正（最高优先级）
        self.atk_body.atk_coef_process(self)

    def formula(self):
        # 基础攻击力
        base_status = self.equip.get_final_status('torpedo')
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
        return real_atk


class MissileAtk(ATK):
    """导弹攻击"""

    def __init__(self, timer, atk_body, def_list, equip, coef=None, target=None):
        super().__init__(timer, atk_body, def_list, coef, target)
        self.equip = equip

        self.form_coef.update({
            'power': [1, .8, .75, 1, .8],
            'hit': [1.1, 1, .9, 1.2, .75],
            'miss': [.9, 1.2, .9, .8, 1.3],
        })  # 阵型系数
        self.pierce_base = 0  # 穿甲基础值

    def crit_verify(self):
        """暴击检定"""
        if self.get_coef('must_crit') or \
                self.atk_body.get_special_buff('must_crit', self) or \
                self.target.get_special_buff('must_be_crit', self) or \
                self.equip.get_special_buff('must_crit', self):
            self.coef['crit_flag'] = True
            return

        if self.get_coef('must_not_crit') or \
                self.atk_body.get_special_buff('must_not_crit', self) or \
                self.target.get_special_buff('must_not_be_crit', self) or \
                self.equip.get_special_buff('must_not_crit', self):
            self.coef['crit_flag'] = False
            return

        # 基础暴击率
        crit = 0.05 + (self.atk_body.affection - 50) * 0.001 + \
               self.get_coef_value('crit') + \
               self.atk_body.get_atk_buff('crit', self)[1] + \
               self.atk_body.get_final_status('luck') * 0.0016 + \
               self.target.get_atk_buff('be_crit', self)[1]

        # 阵型暴击率补正
        crit += self.get_form_coef('crit', self.atk_body.get_form()) + \
                self.get_form_coef('be_crit', self.target.get_form())

        crit = cap(crit)
        verify = np.random.random()
        if verify <= crit:
            self.coef['crit_flag'] = True
            return
        else:
            self.coef['crit_flag'] = False
            return

    def hit_verify(self):
        """导弹攻击命中检定，含导弹装备命中率、必中buff"""
        # 技能、战术判定
        if self.skill_hit_verify():
            return

        # 外部命中率修改
        if self.outer_hit_verify():
            return

        # 基础命中率
        accuracy = self.atk_body.get_final_status('accuracy')
        evasion = self.target.get_final_status('evasion')

        # 梯形锁定减少闪避
        if self.target.get_special_buff('t_lock'):
            evasion *= 0.9  # todo 数值未知

        hit_rate = accuracy / max(1, evasion) / 2

        # 阵型命中率补正
        hit_rate *= self.get_form_coef('hit', self.atk_body.get_form()) / \
                    self.get_form_coef('miss', self.target.get_form())

        # 索敌补正
        if self.atk_body.get_recon_flag():
            hit_rate *= 1.05
        if self.target.get_recon_flag():
            hit_rate *= 0.95

        # 导弹补正
        hit_rate += 0.5

        # 船型补正
        d_size = self.atk_body.size - self.target.size
        hit_rate *= 1 - max(0, d_size * 0.1)

        # 装备补正
        _, hitrate_bias = self.equip.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias

        # 好感补正
        hit_rate += (self.atk_body.affection - 50) * 0.001
        hit_rate -= (self.target.affection - 50) * 0.001

        # 技能补正
        _, hitrate_bias = self.atk_body.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias
        _, hitrate_bias = self.target.get_atk_buff('miss_rate', self)
        hit_rate -= hitrate_bias

        hit_rate = cap(hit_rate)
        verify = np.random.random()
        if verify <= hit_rate:
            self.coef['hit_flag'] = True
            return
        else:
            self.coef['hit_flag'] = False
            return

    def skill_hit_verify(self):
        """必中/护盾等技能/战术判定"""
        # 护盾
        if self.target.get_special_buff('shield', self):
            self.coef['hit_flag'] = False
            return True

        # 技能必中
        if self.get_coef('must_hit') or \
                self.atk_body.get_special_buff('must_hit', self) or \
                self.equip.get_special_buff('must_hit', self):
            self.coef['hit_flag'] = True
            return True

        # 技能必不中
        if self.get_coef('must_not_hit') or \
                self.target.get_special_buff('must_not_hit', self) or \
                self.equip.get_special_buff('must_not_hit', self):
            self.coef['hit_flag'] = False
            return True

        return False


    def formula(self):
        # 基础攻击力
        base_atk = self.atk_body.get_final_status('fire', equip=False) + \
                   3 * self.equip.get_final_status('fire')

        # 实际威力
        real_atk = (base_atk *
                    self.coef['form_coef'] *
                    self.coef['skill_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])
        return real_atk

    def real_damage(self, real_atk):
        if real_atk is None:
            raise ValueError(f'Formula of "{type(self).__name__}" is not defined!')

        # 目标装甲
        ignore_scale, ignore_bias = self.atk_body.get_atk_buff('ignore_armor', self)  # 无视装甲
        def_armor = self.target.get_final_status('armor') * \
                    (1 + ignore_scale) + ignore_bias
        def_armor = max(0, def_armor)

        # 实际伤害
        if def_armor <= 50:
            armor_coef = 1 - def_armor ** 2 / 12500 + self.coef['pierce_coef']
        else:
            armor_coef = (def_armor - 150) ** 2 / 12500 + self.coef['pierce_coef']
        armor_coef = max(0.1, armor_coef)
        real_dmg = np.ceil(real_atk * armor_coef)

        if real_dmg <= 0:
            if np.random.random() < 0.5:  # 50% 跳弹
                return 0
            else:  # 50% 擦伤
                real_dmg = np.ceil(
                    min(real_atk, self.target.status['health']) * 0.1
                )
        return real_dmg


class AntiSubAtk(ATK):
    """反潜攻击"""

    def __init__(self, timer, atk_body, def_list, coef=None, target=None):
        super().__init__(timer, atk_body, def_list, coef, target)

        self.form_coef.update({
            'power': [1, 1, 1, 1, 1],
            'hit': [1, 1, 1, 1, 1.2],
            'miss': [1, 1, 1, 1, 1.2],
        })  # 阵型系数
        self.pierce_base = 2  # 穿甲基础值

    def formula(self):
        # 基础攻击力
        s_antisub = self.atk_body.get_final_status('antisub', equip=False)  # 裸反潜
        e_antisub = self.atk_body.get_equip_status('antisub', equiptype=DepthMine)  # 深投反潜
        sonar = 1 + (self.atk_body.get_equip_status('antisub') - e_antisub) / 10  # 声纳系数
        base_atk = np.floor(
            (pow(e_antisub, 1/3) * 20 + s_antisub / 3) * sonar
        )

        # 实际威力
        real_atk = (base_atk *
                    self.coef['skill_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])
        return real_atk


class AirAntiSubAtk(AntiSubAtk, AirAtk):
    """航空反潜攻击"""

    def __init__(self, timer, atk_body, def_list, coef=None, target=None):
        super().__init__(timer, atk_body, def_list, coef, target)
        self.pierce_base = 10  # 穿甲基础值

    def formula(self):
        # 基础攻击力
        s_antisub = self.atk_body.get_final_status('antisub', equip=False)  # 裸反潜
        e_antisub = self.atk_body.get_equip_status('antisub')  # 装备反潜
        recon = self.atk_body.get_final_status('recon')  # 索敌
        base_atk = s_antisub + e_antisub * 2 + recon / 2

        # 实际威力
        real_atk = (base_atk *
                    self.coef['skill_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])
        return real_atk


class TorpedoAtk(ATK):
    """鱼雷攻击"""

    def __init__(self, timer, atk_body, def_list, coef=None, target=None):
        super().__init__(timer, atk_body, def_list, coef, target)

        self.form_coef.update({
            'power': [1, .9, .8, 1, .8],
            'hit': [1, 1.1, .9, 1.2, .5],
            'miss': [.9, 1.2, .9, .8, 1.3],
        })  # 阵型系数
        self.pierce_base = 1  # 穿甲基础值

    def formula(self):
        # 基础攻击力
        base_atk = self.atk_body.get_final_status('torpedo') + 5

        # 实际威力
        real_atk = (base_atk *
                    self.coef['form_coef'] *
                    self.coef['skill_coef'] *
                    self.coef['dir_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])
        return real_atk


class NormalAtk(ATK):
    """普通炮击"""

    def __init__(self, timer, atk_body, def_list, coef=None, target=None):
        super().__init__(timer, atk_body, def_list, coef, target)

        self.form_coef.update({
            'power': [1, .8, .75, 1, .8],
            'hit': [1.1, 1, .9, 1.2, .75],
            'miss': [.9, 1.2, .9, .8, 1.3],
        })  # 阵型系数

    def formula(self):
        # 基础攻击力
        base_atk = self.atk_body.get_final_status('fire') + 5

        # 实际威力
        real_atk = (base_atk *
                    self.coef['form_coef'] *
                    self.coef['skill_coef'] *
                    self.coef['dir_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])
        return real_atk


class MagicAtk(NormalAtk):
    """技能特殊攻击(只包含固定伤害，不过甲)"""

    def hit_verify(self):
        # 护盾
        if self.target.get_special_buff('shield', self):
            self.coef['hit_flag'] = False
            return

        # 大角度
        if self.target.get_strategy_buff('strategy_shield', self):
            self.coef['hit_flag'] = False
            return

        self.coef['hit_flag'] = True
        return

    def formula(self):
        return 0

    def real_damage(self, real_atk):
        if real_atk is None:
            raise ValueError(f'Formula of "{type(self).__name__}" is not defined!')
        return real_atk


class SpecialAtk(ATK):
    """技能特殊攻击(不会触发普通攻击可以触发的特效)"""

    def __init__(self, timer, atk_body, def_list, coef=None, target=None):
        super().__init__(timer, atk_body, def_list, coef, target)

        self.form_coef.update({
            'power': [1, .8, .75, 1, .8],
            'hit': [1.1, 1, .9, 1.2, .75],
            'miss': [.9, 1.2, .9, .8, 1.3],
        })  # 阵型系数

    def formula(self):
        # 基础攻击力
        base_atk = self.atk_body.get_final_status('fire') + 5

        # 实际威力
        real_atk = (base_atk *
                    self.coef['form_coef'] *
                    self.coef['skill_coef'] *
                    self.coef['dir_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])
        return real_atk

    def end_atk(self, damage_flag, damage_value):
        hit_back = None
        chase_atk = None
        if not damage_flag:
            self.timer.report('miss')
        else:
            self.atk_body.atk_hit('atk_hit', self)
            self.timer.report(damage_value)

        self.atk_body.remove_during_buff()
        self.target.remove_during_buff()
        return hit_back, chase_atk


class AirNormalAtk(NormalAtk, AirAtk):
    """炮击战航空炮击"""

    def hit_verify(self):
        """命中检定"""
        # 技能、战术判定
        if self.skill_hit_verify():
            return

        # 外部命中率修改
        if self.outer_hit_verify():
            return

        # 基础命中率
        accuracy = self.atk_body.get_final_status('accuracy')

        hit_rate = accuracy / 50 / 2
        hit_rate = min(1, hit_rate)

        # 阵型命中率补正
        hit_rate *= self.get_form_coef('hit', self.atk_body.get_form()) / \
                    self.get_form_coef('miss', self.target.get_form())

        # 索敌补正
        if self.atk_body.get_recon_flag():
            hit_rate *= 1.05
        if self.target.get_recon_flag():
            hit_rate *= 0.95

        # 制空补正
        hit_rate *= 1 + get_air_hit_coef(self.atk_body.get_air_con_flag())

        # 船型补正
        aa_value = self.get_anti_air_def()
        if self.target.size == 3:
            aa_base = 1500
            mul_rate = 1
        elif self.target.size == 2:
            aa_base = 375
            mul_rate = 0.75
        else:
            aa_base = 150
            mul_rate = 0.5
        aa_hit_coef = aa_base / (aa_base + aa_value)
        hit_rate *= aa_hit_coef * mul_rate

        # 好感补正
        hit_rate += (self.atk_body.affection - 50) * 0.001
        hit_rate -= (self.target.affection - 50) * 0.001

        # 技能补正
        _, hitrate_bias = self.atk_body.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias
        _, hitrate_bias = self.target.get_atk_buff('miss_rate', self)
        hit_rate -= hitrate_bias

        hit_rate = cap(hit_rate)
        verify = np.random.random()
        if verify <= hit_rate:
            self.coef['hit_flag'] = True
            return
        else:
            self.coef['hit_flag'] = False

    def process_coef(self):
        # 制空系数
        _, self.coef['air_con_coef'] = get_air_coef(self.timer.air_con_flag,
                                                    self.atk_body.side)
        # 阵型系数
        self.coef['form_coef'] = self.get_form_coef('power', self.atk_body.get_form())

        # 技能系数
        skill_scale, _ = self.atk_body.get_atk_buff('air_atk_buff', self)
        self.coef['skill_coef'] = 1 + skill_scale

        # 船损系数
        self.coef['dmg_coef'] = self.get_dmg_coef()

        # 弹损系数
        self.coef['supply_coef'] = self.get_supply_coef()

        # 暴击系数
        if self.coef['crit_flag']:
            _, crit_bias = self.atk_body.get_atk_buff('crit_coef', self)
            self.coef['crit_coef'] = 1.5 + crit_bias
        else:
            self.coef['crit_coef'] = 1.

        # 浮动系数
        self.coef['random_coef'] = np.random.uniform(self.random_range[0],
                                                     self.random_range[1])

        # 穿甲系数
        _, pierce_bias = self.atk_body.get_atk_buff('pierce_coef', self)
        self.coef['pierce_coef'] = 1. + pierce_bias

        # 攻击者对系数进行最终修正（最高优先级）
        self.atk_body.atk_coef_process(self)

    def formula(self):
        # 基础攻击力
        fire = self.atk_body.get_final_status('fire')
        bomb = self.atk_body.get_final_status('bomb')
        torpedo = self.atk_body.get_final_status('torpedo')
        ignore_scale, ignore_bias = self.atk_body.get_atk_buff('ignore_antiair', self)  # 无视对空
        target_anti_air = self.target.get_final_status('antiair') * \
                          (1 + ignore_scale) + ignore_bias  # 本体总对空
        target_anti_air = max(0, target_anti_air)
        random_weight = np.random.random()
        base_atk = (fire + 2 * bomb + torpedo)\
                   * max(0, 1 - target_anti_air * random_weight / 150)\
                   + 35

        # 实际威力
        real_atk = (base_atk *
                    self.coef['air_con_coef'] *
                    self.coef['form_coef'] *
                    self.coef['skill_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])
        return real_atk

    def final_damage(self, damage):
        """航空炮击终伤"""

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

        # 额外伤害
        _, extra_damage = self.atk_body.get_atk_buff('extra_damage', self)
        damage += extra_damage

        # 终伤增伤系数
        for buff_scale in self.atk_body.get_final_damage_buff(self):
            damage = np.ceil(damage * (1 + buff_scale))
        buff_scale = self.get_coef('final_damage_buff')
        if buff_scale:
            damage = np.ceil(damage * (1 + buff_scale))

        # 终伤减伤系数
        for debuff_scale in self.target.get_final_damage_debuff(self):
            damage = np.ceil(damage * (1 + debuff_scale))
        buff_scale = self.get_coef('final_damage_debuff')
        if buff_scale:
            damage = np.ceil(damage * (1 + buff_scale))

        # 挡枪减伤
        tank_damage_debuff = self.get_coef('tank_damage_debuff')
        if tank_damage_debuff is not None:
            damage = np.ceil(damage * (1 + tank_damage_debuff))

        # 战术终伤
        buff_scale = self.atk_body.get_strategy_value('final_damage_buff', self)
        if buff_scale:
            damage = np.ceil(damage * (1 + buff_scale))
        debuff_scale = self.target.get_strategy_value('final_damage_debuff', self)
        if debuff_scale:
            damage = np.ceil(damage * (1 + debuff_scale))

        # 技能伤害减免
        _, reduce_damage = self.target.get_atk_buff(name='reduce_damage',
                                                    atk=self,
                                                    damage=damage)
        damage -= reduce_damage

        return max(0, damage)


class NightAtk(ATK):
    """夜战系数"""

    def __init__(self, timer, atk_body, def_list, coef=None, target=None,
                 *args, **kwargs):
        super().__init__(timer, atk_body, def_list, coef=coef, target=target,
                         *args, **kwargs)

        self.form_coef.update({
            'power': [1.1, .9, 1, 1, 1],
            'hit': [1, 1.1, 1, 1.2, 1],
            'miss': [1, 1.1, .9, 1, 1.2],
        })  # 阵型系数
        self.dir_coef = [1, 1, 1, 1]  # 航向系数，按照优同反劣顺序

    def real_damage(self, real_atk):
        if real_atk is None:
            raise ValueError(f'Formula of "{type(self).__name__}" is not defined!')

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
                    min(real_atk, self.target.status['health']) * 0.1
                )
        return real_dmg


class NightNormalAtk(NightAtk, NormalAtk):
    """夜战普通炮击"""

    def __init__(self, timer, atk_body, def_list, coef=None, target=None):
        super().__init__(timer, atk_body, def_list, coef, target)
        self.random_range = [1.2, 1.8]  # 浮动系数上下限

    def formula(self):
        # 基础攻击力
        base_atk = self.atk_body.get_final_status('fire') + 10

        # 实际威力
        real_atk = (base_atk *
                    self.coef['form_coef'] *
                    self.coef['skill_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])
        return real_atk


class NightFirelAtk(NightNormalAtk):
    """夜战纯火巡洋舰炮击"""

    def __init__(self, timer, atk_body, def_list, coef=None, target=None):
        super().__init__(timer, atk_body, def_list, coef, target)
        self.random_range = [2.4, 3.6]  # 浮动系数上下限


class NightFireTorpedolAtk(NightNormalAtk):
    """夜战火雷连击"""

    def __init__(self, timer, atk_body, def_list, coef=None, target=None):
        super().__init__(timer, atk_body, def_list, coef, target)
        self.pierce_base = 0.8  # 穿甲基础值

    def formula(self):
        # 基础攻击力
        base_atk = self.atk_body.get_final_status('fire') + \
                   self.atk_body.get_final_status('torpedo') + \
                   10

        # 实际威力
        real_atk = (base_atk *
                    self.coef['form_coef'] *
                    self.coef['skill_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])
        return real_atk


class NightTorpedoAtk(NightAtk, TorpedoAtk):
    """夜战纯雷击"""

    def __init__(self, timer, atk_body, def_list, coef=None, target=None):
        super().__init__(timer, atk_body, def_list, coef, target)
        self.random_range = [2.4, 3]  # 浮动系数上下限
        self.pierce_base = 1  # 穿甲基础值

    def formula(self):
        # 基础攻击力
        base_atk = self.atk_body.get_final_status('torpedo') + 10

        # 实际威力
        real_atk = (base_atk *
                    self.coef['form_coef'] *
                    self.coef['skill_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])
        return real_atk


class NightMissileAtk(NightAtk, MissileAtk):
    """夜战导弹攻击"""

    def __init__(self, timer, atk_body, def_list, equip, coef=None, target=None):
        super().__init__(timer, atk_body, def_list,
                         equip=equip, coef=coef, target=target)
        self.random_range = [1.2, 1.5]  # 浮动系数上下限
        self.pierce_base = 1  # 穿甲基础值


class NightAntiSubAtk(AntiSubAtk, NightAtk):
    """夜战反潜"""

    def final_damage(self, damage):
        damage = np.ceil(damage * 0.1)

        # 额外伤害
        _, extra_damage = self.atk_body.get_atk_buff('extra_damage', self)
        damage += extra_damage

        # 终伤增伤系数
        for buff_scale in self.atk_body.get_final_damage_buff(self):
            damage = np.ceil(damage * (1 + buff_scale))
        buff_scale = self.get_coef('final_damage_buff')
        if buff_scale:
            damage = np.ceil(damage * (1 + buff_scale))

        # 终伤减伤系数
        for debuff_scale in self.target.get_final_damage_debuff(self):
            damage = np.ceil(damage * (1 + debuff_scale))
        buff_scale = self.get_coef('final_damage_debuff')
        if buff_scale:
            damage = np.ceil(damage * (1 + buff_scale))

        # 挡枪减伤
        tank_damage_debuff = self.get_coef('tank_damage_debuff')
        if tank_damage_debuff is not None:
            damage = np.ceil(damage * (1 + tank_damage_debuff))

        # 战术终伤
        buff_scale = self.atk_body.get_strategy_value('final_damage_buff', self)
        if buff_scale:
            damage = np.ceil(damage * (1 + buff_scale))
        debuff_scale = self.target.get_strategy_value('final_damage_debuff', self)
        if debuff_scale:
            damage = np.ceil(damage * (1 + debuff_scale))

        # 技能伤害减免
        _, reduce_damage = self.target.get_atk_buff(name='reduce_damage',
                                                    atk=self,
                                                    damage=damage)
        damage -= reduce_damage

        return max(0, damage)


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
                        for tmp_equip in ship.equipment
                        if isinstance(tmp_equip, (Fighter, Bomber, DiveBomber))])
    eloc_list = np.array([tmp_equip.enum - 1
                          for tmp_equip in ship.equipment
                          if isinstance(tmp_equip, (Fighter, Bomber, DiveBomber))])
    if not len(eloc_list):
        return 0

    actual_flight = actual_flight[eloc_list]
    buff_scale, _, buff_bias = ship.get_buff('air_con_buff')

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


def get_air_hit_coef(air_con_flag):
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
            if isinstance(tmp_equip, Plane):
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
            equip_aa_coef = tmp_equip.get_final_status('aa_coef')
            if equip_aa_coef != 0:
                anti_air += tmp_equip.get_final_status('antiair')
                aa_coef = max(equip_aa_coef, aa_coef)
    return anti_air * aa_coef


def get_scaled_anti_air(ship):
    """获取(装备防空*防空倍率)之和"""
    anti_air = 0
    for tmp_equip in ship.equipment:
        equip_aa = tmp_equip.get_final_status('antiair')
        equip_aa_scale = tmp_equip.get_final_status('aa_scale')
        anti_air += 2.5 * equip_aa * equip_aa_scale
    return anti_air


if __name__ == "__main__":
    pass
