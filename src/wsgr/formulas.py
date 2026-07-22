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
           'LongMissileAtk',
           'AntiSubAtk',
           'AirAntiSubAtk',
           'TorpedoAtk',
           'NormalAtk',
           'MagicAtk',
           'SpecialAtk',
           'AirNormalAtk',
           'NightAtk',
           'NightNormalAtk',
           'NightFireAtk',
           'NightFireTorpedoAtk',
           'NightTorpedoAtk',
           'NightMissileAtk',
           'NightAirAtk',
           'NightAntiSubAtk'
           ]


# attack types
class ATK(Time):
    """攻击总类"""

    def __init__(self, timer, source, def_list, coef=None, target=None,
                 *args, **kwargs):
        super().__init__(timer)
        self.atk_name = '攻击'
        self.source = source
        self.def_list = def_list  # 可被攻击目标列表

        self.target = target  # 攻击目标，可被更改
        self.changeable = True  # 攻击目标是否可被更改

        self.coef = {}
        if coef is not None:
            self.coef.update(coef)  # 伤害计算相关参数

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

    def __repr__(self, atk_info=None):
        source_name = (f"[{'我方' if self.source.side == 1 else '敌方'}"
                       f"{self.source.loc}号位]"
                       f"{self.source.status['name']}")
        target_name = (f"[{'我方' if self.target.side == 1 else '敌方'}"
                       f"{self.target.loc}号位]"
                       f"{self.target.status['name']}") \
            if self.target is not None else '未确定'
        if atk_info is None:
            atk_info = self.atk_name if hasattr(self, 'atk_name') else type(self).__name__
        return f"{source_name} -> {target_name} ({atk_info})"

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
            return self.end_atk(damage_flag, 'miss', False)

        real_atk = self.formula()
        damage = self.real_damage(real_atk)
        if damage == 0:
            return self.end_atk(damage_flag, 'jump', False)

        damage_flag = True
        damage = self.final_damage(damage)
        sink = self.target.get_damage(damage)
        return self.end_atk(damage_flag, damage, sink)

    def target_init(self):
        """决定攻击目标，技能可以影响优先目标"""
        if self.target is not None:
            return self.target

        # 优先站位攻击
        prior = self.source.get_prior_loc_target(self.def_list)
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

        self.source.atk_hit('give_atk', self)
        self.target.atk_hit('get_atk', self)

    def set_coef(self, coef):
        if coef is not None:
            self.coef.update(coef)

    def process_coef(self):
        # 阵型系数
        self.coef['form_coef'] = self.get_form_coef('power', self.source.get_form())

        # 技能系数
        skill_scale, _ = self.source.get_atk_buff('power_buff', self)
        self.coef['skill_coef'] = 1 + skill_scale
        skill_scale = self.get_coef_value('power_buff')
        self.coef['skill_coef'] *= (1 + skill_scale)

        # 航向系数
        self.coef['dir_coef'] = self.get_dir_coef(self.source.get_dir_flag())

        # 船损系数
        self.coef['dmg_coef'] = self.get_dmg_coef()

        # 弹损系数
        self.coef['supply_coef'] = self.get_supply_coef()

        # 暴击系数
        if self.coef['crit_flag']:
            _, crit_bias = self.source.get_atk_buff('crit_coef', self)
            crit_bias += self.get_coef_value('crit_coef')
            self.coef['crit_coef'] = 1.5 + crit_bias
        else:
            self.coef['crit_coef'] = 1.

        # 浮动系数
        if isinstance(self, NormalAtk):  # 炮击战普通炮击，结算超重弹
            _, equip_bias = self.source.get_atk_buff('uplimit_buff', self)
        else:
            equip_bias = 0
        self.coef['random_coef'] = np.random.uniform(self.random_range[0],
                                                     self.random_range[1] + equip_bias)

        # 穿甲系数
        _, pierce_bias = self.source.get_atk_buff('pierce_coef', self)
        self.coef['pierce_coef'] = self.pierce_base + pierce_bias

        # 攻击者对系数进行最终修正（最高优先级）
        self.source.atk_coef_process(self)

    def get_coef(self, name):
        """获取指定名称的参数，通常为bool值"""
        return self.coef.get(name, None)

    def get_coef_value(self, name):
        """获取指定名称的参数值，通常为float值"""
        return self.coef.get(name, 0)

    def get_form_coef(self, name, form_num):
        """获取阵型系数"""
        coef = self.form_coef.get(name)[form_num - 1]
        return coef

    def get_dir_coef(self, dir_num):
        if self.get_coef('ignore_dir_coef'):
            return 1.
        elif self.source.get_special_buff('ignore_dir_coef', self):
            return 1.
        return self.dir_coef[dir_num - 1]

    def get_dmg_coef(self):
        if self.get_coef('ignore_damaged'):
            return 1.
        elif self.source.get_special_buff('ignore_damaged', self):
            return 1.
        elif self.source.damaged == 1:
            return 1.
        elif self.source.damaged == 2:
            return .6
        else:
            return .3

    def get_supply_coef(self):
        if self.get_coef('ignore_supply'):
            return 1.
        elif self.source.get_special_buff('ignore_supply', self):
            return 1.
        else:
            return min(1., self.source.supply_ammo * 2. / 10.)

    def crit_verify(self):
        """暴击检定"""
        if self.get_coef('must_crit') or \
                self.source.get_special_buff('must_crit', self) or \
                self.target.get_special_buff('must_be_crit', self):
            self.coef['crit_flag'] = True
            return

        if self.get_coef('must_not_crit') or \
                self.source.get_special_buff('must_not_crit', self) or \
                self.target.get_special_buff('must_not_be_crit', self):
            self.coef['crit_flag'] = False
            return

        # 基础暴击率
        crit = 0.05 + (self.source.affection - 50) * 0.001 + \
               self.get_coef_value('crit') + \
               self.source.get_atk_buff('crit', self)[1] + \
               self.source.get_final_status('luck') * 0.0016 + \
               self.target.get_atk_buff('be_crit', self)[1]

        # 阵型暴击率补正
        crit += self.get_form_coef('crit', self.source.get_form()) + \
                self.get_form_coef('be_crit', self.target.get_form())

        crit = cap(crit)
        verify = np.random.random()
        if verify <= crit:
            self.coef['crit_flag'] = True
            return
        else:
            self.coef['crit_flag'] = False
            return

    @property
    def base_hit_rate(self):
        """基础命中率"""
        if self.target is None:  # 此逻辑仅供debug查看使用
            return 'Target not specified'

        accuracy = self.source.get_final_status('accuracy')
        ignore_scale, ignore_bias = self.source.get_atk_buff('ignore_evasion', self)  # 无视回避
        evasion = self.target.get_final_status('evasion') * \
                  (1 + ignore_scale) + ignore_bias

        # 梯形锁定减少闪避
        if self.target.get_special_buff('t_lock'):
            evasion *= 0.6

        hit_rate = accuracy / max(1, evasion) / 2
        return hit_rate

    @property
    def hit_special_coef(self):
        """攻击特有补正"""
        return 0.

    @ property
    def hit_shipsize_coef(self):
        """船型补正闪避系数"""
        return 1.

    @property
    def hit_form_correction(self):
        """单纵、复纵额外补正"""
        if self.target is None:  # 此逻辑仅供debug查看使用
            return 'Target not specified'

        add = 0
        if self.target.get_form() == 2:
            add -= 0.05
        from src.wsgr.phase import SecondShellingPhase
        if self.source.get_form() == 1 and \
                isinstance(self.timer.phase, SecondShellingPhase):
            add = 0.05  # todo 待验证，次轮单纵可能取消复纵减益
        return add

    @property
    def hit_affection_coef(self):
        """好感补正"""
        if self.target is None:  # 此逻辑仅供debug查看使用
            return 'Target not specified'
        return (self.source.affection - self.target.affection) * 0.001

    @property
    def hit_skill_coef(self):
        """技能补正"""
        if self.target is None:  # 此逻辑仅供debug查看使用
            return 'Target not specified'
        hit_rate = 0
        _, hitrate_bias = self.source.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias
        _, hitrate_bias = self.target.get_atk_buff('miss_rate', self)
        hit_rate -= hitrate_bias
        return hit_rate

    def hit_verify(self):
        """命中检定"""
        # 技能、战术判定
        if self.skill_hit_verify():
            return

        # 外部命中率修改
        if self.outer_hit_verify():
            return

        # 基础命中率
        hit_rate = self.base_hit_rate

        # 阵型命中率补正
        hit_rate *= self.get_form_coef('hit', self.source.get_form()) / \
                    self.get_form_coef('miss', self.target.get_form())

        # 索敌补正
        if self.source.get_recon_flag():
            hit_rate += .05
        if self.target.get_recon_flag():
            hit_rate -= .05

        hit_rate += self.hit_special_coef     # 攻击特有补正
        hit_rate *= self.hit_shipsize_coef    # 船型补正
        hit_rate += self.hit_form_correction  # 单纵、复纵额外补正
        hit_rate += self.hit_affection_coef   # 好感补正
        hit_rate += self.hit_skill_coef       # 技能补正(部分攻击含装备补正)

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
                self.source.get_special_buff('must_hit', self):
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

    def formula(self):
        pass

    def real_damage(self, real_atk):
        if real_atk is None:
            raise ValueError(f'Formula of "{type(self).__name__}" is not defined!')

        # 实际伤害
        ignore_scale, ignore_bias = self.source.get_atk_buff('ignore_armor', self)  # 无视装甲
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
        _, extra_damage = self.source.get_atk_buff('extra_damage', self)
        damage += extra_damage

        # 终伤增伤系数
        for buff_scale in self.source.get_final_damage_buff(self):
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
        buff_scale = self.source.get_strategy_value('final_damage_buff', self)
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

    def end_atk(self, damage_flag, damage_value, sink):
        """
        攻击结束时点，进行受伤时点效果、反击等
        :param damage_flag: 是否受到了伤害
        :param damage_value: 伤害记录
        :param sink: 是否被击沉
        """
        hit_back = None
        chase_atk = None
        if not damage_flag:
            assert sink is False
            self.timer.report_damage('miss', sink)
        else:
            self.source.atk_hit('atk_hit', self)
            hit_back = self.target.atk_hit('atk_be_hit', self)
            for tmp_buff in self.timer.queue['chase']:
                if tmp_buff.is_active(self):
                    chase_atk = tmp_buff.activate(self)
                    break
            self.timer.report_damage(damage_value, sink)

        self.source.remove_during_buff()
        self.target.remove_during_buff()
        return hit_back, chase_atk


class SupportAtk(ATK):
    """支援攻击"""
    def __init__(self, timer, source, def_list, limit: list, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)
        self.limit = limit  # 攻击上下限
        self.atk_name = '支援攻击'

    def start(self):
        self.timer.set_atk(self)
        damage = self.formula()
        damage_flag = bool(damage)
        sink = self.target.get_damage(damage)
        return self.end_atk(damage_flag, damage, sink)

    def formula(self):
        damage = np.random.uniform(self.limit[0], self.limit[1])
        return np.ceil(damage)

    def end_atk(self, damage_flag, damage_value, sink):
        hit_back = None
        chase_atk = None
        if not damage_flag:
            assert sink is False
            self.timer.report_damage('miss', sink)
        else:
            self.timer.report_damage(damage_value, sink)
        return hit_back, chase_atk


class AirAtk(ATK):
    """航空攻击，包含航空战AirStrikeAtk、炮击战AirNormalAtk、炮击战航空反潜AirAntiSubAtk"""
    def __init__(self, timer, source, def_list, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)
        self.atk_name = '航空攻击'
        self.equip = None

    def get_anti_air_def(self):
        """减伤对空"""
        ignore_scale, ignore_bias = self.source.get_atk_buff('ignore_antiair', self)  # 无视对空
        target_anti_air = self.target.get_final_status('antiair', equip=False) * \
                          (1 + ignore_scale) + ignore_bias  # 本体裸对空
        target_anti_air = max(0, target_anti_air)
        aa_value = target_anti_air + self.get_scaled_anti_air()
        return max(0, aa_value)

    def get_scaled_anti_air(self):
        """获取(装备防空*防空倍率)之和"""
        anti_air = 0
        for tmp_equip in self.target.equipment:
            equip_aa = tmp_equip.get_final_status('antiair')
            equip_aa_scale = tmp_equip.get_final_status('aa_scale')
            anti_air += 2.5 * equip_aa * equip_aa_scale
        return anti_air

    def get_air_coef(self):
        """制空命中、伤害系数"""
        air_con_flag = self.source.get_air_con_flag()
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


class AirStrikeAtk(AirAtk):
    """航空战航空攻击"""
    def __init__(self, timer, source, def_list, equip, coef,
                 target=None):
        super().__init__(timer, source, def_list, coef, target)
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
            return self.end_atk(damage_flag, 'miss', False)

        if self.coef['plane_rest'] == 0:
            return self.end_atk(damage_flag, 'miss', False)

        real_atk = self.formula()
        damage = self.real_damage(real_atk)
        if damage == 0:
            return self.end_atk(damage_flag, 'jump', False)

        damage_flag = True
        damage = self.final_damage(damage)
        sink = self.target.get_damage(damage)
        return self.end_atk(damage_flag, damage, sink)

    def process_coef(self):
        # 制空系数
        self.coef['air_con_coef'] = 1 + self.get_air_coef()

        target_num = self.def_list.index(self.target)
        self.coef['anti_num'][target_num] += 1
        anti_num = self.coef['anti_num'][target_num]
        aa_fall = self.get_anti_air_fall(anti_num)  # 防空击坠

        # 最大击坠量不超过实际放飞量
        actual_fall = min(self.coef['actual_flight'],
                          self.coef['air_con_fall'] + aa_fall)

        # 减少击坠技能
        fall_scale, fall_bias = self.source.get_atk_buff('fall_rest', self)
        actual_fall = np.ceil(actual_fall * (1 + fall_scale) + fall_bias)

        # 击坠结算与本次剩余载机量计算
        self.equip.fall(actual_fall)
        self.coef['plane_rest'] = self.coef['actual_flight'] - actual_fall

        # 船损系数
        self.coef['dmg_coef'] = self.get_dmg_coef()

        # 弹损系数
        self.coef['supply_coef'] = self.get_supply_coef()

        # 暴击系数
        if self.coef['crit_flag']:
            _, crit_bias = self.source.get_atk_buff('crit_coef', self)
            self.coef['crit_coef'] = 1.5 + crit_bias
        else:
            self.coef['crit_coef'] = 1.

        # 浮动系数
        self.coef['random_coef'] = np.random.uniform(self.random_range[0],
                                                     self.random_range[1])

        # 攻击者对系数进行最终修正（最高优先级）
        self.source.atk_coef_process(self)

    def get_anti_air_fall(self, anti_num):
        """计算防空击坠"""
        ignore_scale, ignore_bias = self.source.get_atk_buff('ignore_antiair', self)  # 无视对空
        target_anti_air = self.target.get_final_status('antiair', equip=False) * \
                          (1 + ignore_scale) + ignore_bias  # 本体裸对空
        target_anti_air = max(0, target_anti_air)

        team_anti_air = self.get_team_anti_air()  # 全队对空补正
        team_anti_air *= self.get_form_coef('anti_def', self.target.get_form())

        equip_anti_air = self.target.get_equip_status('antiair')  # 装备对空总和

        aa_value = target_anti_air + team_anti_air + equip_anti_air
        aa_value = max(0, aa_value)

        alpha = np.round(np.random.random(), 2)
        bottom_a = 0.6
        aa_fall = np.floor(np.floor(alpha * aa_value / 10) * bottom_a ** (anti_num - 1))
        self.coef['antiair_fall'] = aa_fall
        return aa_fall

    def get_team_anti_air(self):
        """获取全队补正防空"""
        anti_air = 0
        for tmp_ship in self.def_list:
            ship_anti_air = 0
            aa_coef = 0
            for tmp_equip in tmp_ship.equipment:
                equip_aa_coef = tmp_equip.get_final_status('aa_coef')
                ship_anti_air += tmp_equip.get_final_status('antiair')
                aa_coef = max(equip_aa_coef, aa_coef)
            anti_air += ship_anti_air * aa_coef
        return anti_air

    @property
    def base_hit_rate(self):
        """航空攻击基础命中率"""
        accuracy = self.source.get_final_status('accuracy')
        aa_value = 0.4 * self.get_anti_air_def()
        if self.target.size == 3:
            aa_mult = .2
        elif self.target.size == 2:
            aa_mult = .8
        else:
            aa_mult = 2
        hit_rate = accuracy / max(1, aa_value * aa_mult + accuracy)
        return hit_rate

    @property
    def hit_special_coef(self):
        """攻击特有补正(制空命中加成)"""
        return self.get_air_coef()

    @property
    def hit_shipsize_coef(self):
        """船型补正闪避系数"""
        if self.target is None:  # 此逻辑仅供debug查看使用
            return 'Target not specified'
        return 0.25 + 0.25 * self.target.size

    @property
    def hit_skill_coef(self):
        """技能、装备补正"""
        hit_rate = 0

        # 装备补正(被特殊技能附加在装备上的独立命中补正，装备词条算作技能补正)
        _, hitrate_bias = self.equip.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias

        # 技能补正
        _, hitrate_bias = self.source.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias
        _, hitrate_bias = self.target.get_atk_buff('miss_rate', self)
        hit_rate -= hitrate_bias
        return hit_rate

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
        _, extra_damage = self.source.get_atk_buff('extra_damage', self)
        damage += extra_damage

        # 终伤增伤系数
        for buff_scale in self.source.get_final_damage_buff(self):
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
        buff_scale = self.source.get_strategy_value('final_damage_buff', self)
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
    def __repr__(self, atk_info=None):
        atk_info = f"航空轰炸机-{self.equip.status['name']}"
        return super().__repr__(atk_info)

    def process_coef(self):
        # 技能系数
        skill_scale, _ = self.source.get_atk_buff('air_atk_buff', self)
        self.coef['skill_coef'] = 1 + skill_scale
        skill_scale, _ = self.source.get_atk_buff('air_bomb_atk_buff', self)
        self.coef['skill_coef'] *= (1 + skill_scale)
        skill_scale, _ = self.source.get_atk_buff('power_buff', self)
        self.coef['skill_coef'] *= (1 + skill_scale)

        # 穿甲系数
        _, pierce_bias = self.source.get_atk_buff('pierce_coef', self)
        self.coef['pierce_coef'] = 1. + pierce_bias

        super().process_coef()

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
    def __repr__(self, atk_info=None):
        atk_info = f"航空鱼雷机-{self.equip.status['name']}"
        return super().__repr__(atk_info)

    def process_coef(self):
        # 技能系数
        skill_scale, _ = self.source.get_atk_buff('air_atk_buff', self)
        self.coef['skill_coef'] = 1 + skill_scale
        skill_scale, _ = self.source.get_atk_buff('air_dive_atk_buff', self)
        self.coef['skill_coef'] *= (1 + skill_scale)
        skill_scale, _ = self.source.get_atk_buff('power_buff', self)
        self.coef['skill_coef'] *= (1 + skill_scale)

        # 鱼雷机系数
        self.coef['dive_random_coef'] = np.random.uniform(.5, 1.)

        # 穿甲系数
        _, pierce_bias = self.source.get_atk_buff('pierce_coef', self)
        self.coef['pierce_coef'] = 2. + pierce_bias

        super().process_coef()

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

    def __init__(self, timer, source, def_list, equip, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)
        self.equip = equip

        self.form_coef.update({
            'power': [1, .8, .75, 1, .8],
            'hit': [1.1, 1, .9, 1.2, .75],
            'miss': [.9, 1.2, .9, .8, 1.3],
        })  # 阵型系数
        self.pierce_base = 0  # 穿甲基础值

    def __repr__(self, atk_info=None):
        from src.wsgr.phase import \
            FirstMissilePhase, SecondMissilePhase, LongMissilePhase
        if isinstance(self.timer.phase, FirstMissilePhase):
            atk_info = f"开幕导弹-{self.equip.status['name']}"
        elif isinstance(self.timer.phase, SecondMissilePhase):
            atk_info = f"闭幕导弹-{self.equip.status['name']}"
        elif isinstance(self.timer.phase, LongMissilePhase):
            atk_info = f"远程打击-{self.equip.status['name']}"
        else:
            atk_info = '导弹攻击'
        return super().__repr__(atk_info)

    def crit_verify(self):
        """暴击检定"""
        if self.get_coef('must_crit') or \
                self.source.get_special_buff('must_crit', self) or \
                self.target.get_special_buff('must_be_crit', self) or \
                self.equip.get_special_buff('must_crit', self):
            self.coef['crit_flag'] = True
            return

        if self.get_coef('must_not_crit') or \
                self.source.get_special_buff('must_not_crit', self) or \
                self.target.get_special_buff('must_not_be_crit', self) or \
                self.equip.get_special_buff('must_not_crit', self):
            self.coef['crit_flag'] = False
            return

        # 基础暴击率
        crit = 0.05 + (self.source.affection - 50) * 0.001 + \
               self.get_coef_value('crit') + \
               self.source.get_atk_buff('crit', self)[1] + \
               self.source.get_final_status('luck') * 0.0016 + \
               self.target.get_atk_buff('be_crit', self)[1]

        # 阵型暴击率补正
        crit += self.get_form_coef('crit', self.source.get_form()) + \
                self.get_form_coef('be_crit', self.target.get_form())

        crit = cap(crit)
        verify = np.random.random()
        if verify <= crit:
            self.coef['crit_flag'] = True
            return
        else:
            self.coef['crit_flag'] = False
            return

    @property
    def hit_special_coef(self):
        """导弹攻击特有补正"""
        return 0.5

    @property
    def hit_skill_coef(self):
        """技能、装备补正"""
        hit_rate = 0

        # 装备补正(被特殊技能附加在装备上的独立命中补正，装备词条算作技能补正)
        _, hitrate_bias = self.equip.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias

        # 技能补正
        _, hitrate_bias = self.source.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias
        _, hitrate_bias = self.target.get_atk_buff('miss_rate', self)
        hit_rate -= hitrate_bias
        return hit_rate

    def skill_hit_verify(self):
        """必中/护盾等技能/战术判定"""
        # 护盾
        if self.target.get_special_buff('shield', self):
            self.coef['hit_flag'] = False
            return True

        # 技能必中
        if self.get_coef('must_hit') or \
                self.source.get_special_buff('must_hit', self) or \
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
        base_atk = self.source.get_final_status('fire', equip=False) + \
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
        ignore_scale, ignore_bias = self.source.get_atk_buff('ignore_armor', self)  # 无视装甲
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


class LongMissileAtk(MissileAtk):
    """远程导弹攻击"""

    @property
    def hit_form_correction(self):
        """单纵、复纵额外补正"""
        return 0.

    @property
    def hit_skill_coef(self):
        """技能、装备补正"""
        hit_rate = 0

        # 装备补正(被特殊技能附加在装备上的独立命中补正，装备词条算作技能补正)
        _, hitrate_bias = self.equip.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias

        # 导巡远程打击额外补正
        from src.wsgr.ship import KP
        if isinstance(self.source, KP):
            hit_rate += 0.05

        # 技能补正(在此时只有装备词条等 PrepSkill 或 CommonSkill 技能被结算)
        _, hitrate_bias = self.source.get_atk_buff('hit_rate', self)
        hit_rate += hitrate_bias
        _, hitrate_bias = self.target.get_atk_buff('miss_rate', self)
        hit_rate -= hitrate_bias
        return hit_rate


class AntiSubAtk(ATK):
    """反潜攻击"""

    def __init__(self, timer, source, def_list, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)
        self.atk_name = '反潜攻击'
        self.form_coef.update({
            'power': [1, 1, 1, 1, 1],
            'hit': [1, 1, 1, 1, 1],
            'miss': [.8, 1, 1.2, .8, .9],
        })  # 阵型系数
        self.pierce_base = 2  # 穿甲基础值

    @property
    def base_hit_rate(self):
        """基础命中率"""
        if self.target is None:  # 此逻辑仅供debug查看使用
            return 'Target not specified'

        antisub = self.source.get_final_status('antisub', equip=False)  # 裸反潜
        ignore_scale, ignore_bias = self.source.get_atk_buff('ignore_evasion', self)  # 无视回避
        evasion = self.target.get_final_status('evasion') * \
                  (1 + ignore_scale) + ignore_bias

        hit_rate = antisub / max(1, evasion) / 2
        return hit_rate

    @property
    def hit_affection_coef(self):
        """好感补正"""
        return 0.

    def formula(self):
        # 基础攻击力
        s_antisub = self.source.get_final_status('antisub', equip=False)  # 裸反潜
        e_antisub = self.source.get_equip_status('antisub', equiptype=DepthMine)  # 深投反潜
        sonar = 1 + (self.source.get_equip_status('antisub') - e_antisub) / 10  # 声纳系数
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


class AirAntiSubAtk(AntiSubAtk):
    """航空反潜攻击"""

    def __init__(self, timer, source, def_list, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)
        self.atk_name = '航空反潜攻击'
        self.pierce_base = 10  # 穿甲基础值

    @property
    def base_hit_rate(self):
        """基础命中率"""
        return ATK.base_hit_rate.fget(self)

    @property
    def hit_affection_coef(self):
        """好感补正"""
        return ATK.hit_affection_coef.fget(self)

    def formula(self):
        # 基础攻击力
        s_antisub = self.source.get_final_status('antisub', equip=False)  # 裸反潜
        e_antisub = self.source.get_equip_status('antisub')  # 装备反潜
        recon = self.source.get_final_status('recon')  # 索敌
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

    def __init__(self, timer, source, def_list, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)
        self.atk_name = '鱼雷攻击'
        self.form_coef.update({
            'power': [1, .9, .8, 1, .8],
            'hit': [1, 1.1, .9, 1.2, .5],
            'miss': [.9, 1.2, .9, .8, 1.3],
        })  # 阵型系数
        self.pierce_base = 1  # 穿甲基础值

    @property
    def hit_shipsize_coef(self):
        """船型补正闪避系数"""
        if self.target is None:  # 此逻辑仅供debug查看使用
            return 'Target not specified'
        return 0.4 + 0.2 * self.target.size

    def formula(self):
        # 基础攻击力
        base_atk = self.source.get_final_status('torpedo') + 5

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

    def __init__(self, timer, source, def_list, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)
        self.form_coef.update({
            'power': [1, .8, .75, 1, .8],
            'hit': [1.1, 1, .9, 1.2, .75],
            'miss': [.9, 1.2, .9, .8, 1.3],
        })  # 阵型系数

    def __repr__(self, atk_info=None):
        from src.wsgr.phase import FirstShellingPhase, SecondShellingPhase
        if self.get_coef('hit_back'):
            atk_info = '反击'
        elif isinstance(self.timer.phase, FirstShellingPhase):
            atk_info = '首轮炮击'
        elif isinstance(self.timer.phase, SecondShellingPhase):
            atk_info = '次轮炮击'
        else:
            atk_info = '普通炮击'
        return super().__repr__(atk_info)

    @property
    def hit_shipsize_coef(self):
        """船型补正闪避系数"""
        if self.target is None:  # 此逻辑仅供debug查看使用
            return 'Target not specified'
        d_size = self.source.size - self.target.size
        return 1 - max(0, d_size * 0.1)

    def formula(self):
        # 基础攻击力
        base_atk = self.source.get_final_status('fire') + 5

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

    def __init__(self, timer, source, def_list, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)

        self.form_coef.update({
            'power': [1, .8, .75, 1, .8],
            'hit': [1.1, 1, .9, 1.2, .75],
            'miss': [.9, 1.2, .9, .8, 1.3],
        })  # 阵型系数

    def formula(self):
        # 基础攻击力
        base_atk = self.source.get_final_status('fire') + 5

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

    def end_atk(self, damage_flag, damage_value, sink):
        hit_back = None
        chase_atk = None
        if not damage_flag:
            assert sink is False
            self.timer.report_damage('miss', sink)
        else:
            self.source.atk_hit('atk_hit', self)
            self.timer.report_damage(damage_value, sink)

        self.source.remove_during_buff()
        self.target.remove_during_buff()
        return hit_back, chase_atk


class AirNormalAtk(NormalAtk, AirAtk):
    """炮击战航空炮击"""

    @property
    def base_hit_rate(self):
        """航空攻击基础命中率"""
        return AirStrikeAtk.base_hit_rate.fget(self)
        # accuracy = self.source.get_final_status('accuracy')
        # aa_value = 0.4 * self.get_anti_air_def()
        # if self.target.size == 3:
        #     aa_mult = .2
        # elif self.target.size == 2:
        #     aa_mult = .8
        # else:
        #     aa_mult = 2
        # hit_rate = accuracy / max(1, aa_value * aa_mult + accuracy)
        # return hit_rate

    # @property
    # def hit_shipsize_coef(self):
    #     """船型补正闪避系数"""
    #     return NormalAtk.hit_shipsize_coef.fget(self)

    def process_coef(self):
        # 制空系数
        self.coef['air_con_coef'] = 1 + self.get_air_coef()
        # 阵型系数
        self.coef['form_coef'] = self.get_form_coef('power', self.source.get_form())

        # 技能系数
        skill_scale, _ = self.source.get_atk_buff('air_atk_buff', self)
        self.coef['skill_coef'] = 1 + skill_scale
        skill_scale, _ = self.source.get_atk_buff('power_buff', self)
        self.coef['skill_coef'] *= (1 + skill_scale)
        skill_scale = self.get_coef_value('power_buff')
        self.coef['skill_coef'] *= (1 + skill_scale)

        # 船损系数
        self.coef['dmg_coef'] = self.get_dmg_coef()

        # 弹损系数
        self.coef['supply_coef'] = self.get_supply_coef()

        # 暴击系数
        if self.coef['crit_flag']:
            _, crit_bias = self.source.get_atk_buff('crit_coef', self)
            self.coef['crit_coef'] = 1.5 + crit_bias
        else:
            self.coef['crit_coef'] = 1.

        # 浮动系数
        self.coef['random_coef'] = np.random.uniform(self.random_range[0],
                                                     self.random_range[1])

        # 穿甲系数
        _, pierce_bias = self.source.get_atk_buff('pierce_coef', self)
        self.coef['pierce_coef'] = 1. + pierce_bias

        # 攻击者对系数进行最终修正（最高优先级）
        self.source.atk_coef_process(self)

    def formula(self):
        # 基础攻击力
        fire = self.source.get_final_status('fire')
        bomb = self.source.get_final_status('bomb')
        torpedo = self.source.get_final_status('torpedo')
        base_atk = (fire + 2 * bomb + torpedo) + 35

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
        _, extra_damage = self.source.get_atk_buff('extra_damage', self)
        damage += extra_damage

        # 终伤增伤系数
        for buff_scale in self.source.get_final_damage_buff(self):
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
        buff_scale = self.source.get_strategy_value('final_damage_buff', self)
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

    def __init__(self, timer, source, def_list, coef=None, target=None,
                 *args, **kwargs):
        super().__init__(timer, source, def_list, coef=coef, target=target,
                         *args, **kwargs)
        self.atk_name = '夜战攻击'
        self.form_coef.update({
            'power': [1.1, .9, 1, 1, 1],
            'hit': [1, 1.1, 1, 1.2, 1],
            'miss': [1, 1.1, .9, 1, 1.2],
        })  # 阵型系数
        self.dir_coef = [1, 1, 1, 1]  # 航向系数，按照优同反劣顺序

    def __repr__(self, atk_info=None):
        atk_info = self.atk_name if hasattr(self, 'atk_name') else type(self).__name__
        return super().__repr__(atk_info)

    @ property
    def hit_shipsize_coef(self):
        """规范化子类船型补正闪避系数"""
        return ATK.hit_shipsize_coef.fget(self)

    def real_damage(self, real_atk):
        """规范化子类伤害结算"""
        return ATK.real_damage(self, real_atk)


class NightNormalAtk(NightAtk, NormalAtk):
    """夜战普通炮击"""

    def __init__(self, timer, source, def_list, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)
        self.atk_name = '夜战普通炮击'
        self.random_range = [1.2, 1.8]  # 浮动系数上下限

    def formula(self):
        # 基础攻击力
        base_atk = self.source.get_final_status('fire') + 10

        # 实际威力
        real_atk = (base_atk *
                    self.coef['form_coef'] *
                    self.coef['skill_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])
        return real_atk


class NightFireAtk(NightNormalAtk):
    """夜战纯火巡洋舰炮击"""

    def __init__(self, timer, source, def_list, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)
        self.atk_name = '夜战火巡炮击'
        self.random_range = [2.4, 3.3]  # 浮动系数上下限


class NightFireTorpedoAtk(NightNormalAtk):
    """夜战火雷连击"""

    def __init__(self, timer, source, def_list, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)
        self.atk_name = '夜战火雷连击'
        self.pierce_base = 0.8  # 穿甲基础值

    def formula(self):
        # 基础攻击力
        base_atk = self.source.get_final_status('fire') + \
                   self.source.get_final_status('torpedo') + \
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

    def __init__(self, timer, source, def_list, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)
        self.atk_name = '夜战雷击'
        self.random_range = [2.4, 3]  # 浮动系数上下限
        self.pierce_base = 1  # 穿甲基础值

    def formula(self):
        # 基础攻击力
        base_atk = self.source.get_final_status('torpedo') + 10

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

    def __init__(self, timer, source, def_list, equip, coef=None, target=None):
        super().__init__(timer, source, def_list,
                         equip=equip, coef=coef, target=target)
        self.random_range = [1.2, 1.5]  # 浮动系数上下限
        self.pierce_base = 1  # 穿甲基础值

    def __repr__(self, atk_info=None):
        atk_info = f"夜战导弹-{self.equip.status['name']}"
        return super().__repr__(atk_info)


class NightAirAtk(NightAtk, AirNormalAtk):
    """夜战航空攻击"""
    def __init__(self, timer, source, def_list, coef=None, target=None):
        super().__init__(timer, source, def_list,
                         coef=coef, target=target)
        self.atk_name = '夜战航空攻击'
        self.random_range = [1.2, 1.5]  # 浮动系数上下限
        self.pierce_base = 1.  # 穿甲基础值


class NightAntiSubAtk(AntiSubAtk, NightAtk):
    """夜战反潜"""

    def __init__(self, timer, source, def_list, coef=None, target=None):
        super().__init__(timer, source, def_list, coef, target)
        self.atk_name = '夜战反潜攻击'
        self.random_range = [0.89, 1.22]  # 浮动系数上下限
        self.pierce_base = .2  # 穿甲基础值

    def formula(self):
        # 基础攻击力
        s_antisub = self.source.get_final_status('antisub', equip=False)  # 裸反潜
        e_antisub = self.source.get_equip_status('antisub', equiptype=DepthMine)  # 深投反潜
        sonar = 1 + (self.source.get_equip_status('antisub') - e_antisub) / 30  # 声纳系数
        base_atk = np.floor(
            (pow(e_antisub + 1, 1/3) * 20 + s_antisub / 3) * sonar
        )

        # 实际威力
        real_atk = (base_atk *
                    self.coef['skill_coef'] *
                    self.coef['dmg_coef'] *
                    self.coef['supply_coef'] *
                    self.coef['crit_coef'] *
                    self.coef['random_coef'])
        return real_atk


def cap(x):
    """将暴击率、命中率等锁定在5%-95%区间"""
    x = max(0.05, x)
    x = min(0.95, x)
    return x


if __name__ == "__main__":
    pass
