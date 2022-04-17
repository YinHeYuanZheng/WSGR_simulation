# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 舰船类

import numpy as np
from src.wsgr.wsgrTimer import Time
from src.wsgr.equipment import *


class Ship(Time):
    """舰船总类"""

    def __init__(self, timer):
        super().__init__(timer)
        self.master = None
        self.cid = '0'  # 编号
        self.type = None  # 船型
        self.size = None  # 量级，大中小型船
        self.function = None  # 功能，主力、护卫舰
        self.status = {
            'name': None,  # 船名
            'country': None,  # 国籍
            'total_health': 0,  # 总耐久
            'health': 0,  # 当前耐久
            'fire': 0,  # 火力
            'torpedo': 0,  # 鱼雷
            'armor': 0,  # 装甲
            'antiair': 0,  # 对空
            'antisub': 0,  # 对潜
            'accuracy': 0,  # 命中
            'evasion': 0,  # 回避
            'recon': 0,  # 索敌
            'speed': 0,  # 航速
            'range': 0,  # 射程, 1: 短; 2: 中; 3: 长; 4: 超长
            'luck': 0,  # 幸运
            'capacity': 0,  # 搭载
            'tag': '',  # 标签(特驱、z系等)
            'supply_oil': 0,  # 补给油耗
            'supply_ammo': 0,  # 补给弹耗
            'repair_oil': 0,  # 修理油耗
            'repair_steel': 0,  # 修理钢耗
        }

        self._skill = []  # 技能(未实例化)
        self.skill = []  # 技能
        self.equipment = []  # 装备
        self.load = []

        self.side = 0  # 敌我识别; 1: 友方; 0: 敌方
        self.loc = 0  # 站位, 1-6
        self.level = 110  # 等级
        self.affection = 200  # 好感

        self.got_damage = 0
        self.damaged = 1  # 耐久状态, 1: 正常; 2: 中破; 3: 大破; 4: 撤退
        self.damage_protect = True  # 耐久保护，大破进击时消失
        self.supply_oil = 1.  # 燃料补给状态
        self.supply_ammo = 1.  # 弹药补给状态

        self.common_buff = []  # 永久面板加成
        self.temper_buff = []  # 临时buff
        self.active_buff = []  # 主动技能buff

        self.act_phase_flag = {
            'AirPhase': False,
            'FirstMissilePhase': False,
            'AntisubPhase': False,
            'FirstTorpedoPhase': False,
            'FirstShellingPhase': True,
            'SecondShellingPhase': True,
            'SecondTorpedoPhase': True,
            'SecondMissilePhase': False,
            'NightPhase': True,
        }  # 可参与阶段

        self.act_phase_indicator = {
            'AirPhase': lambda x: False,
            'FirstMissilePhase': lambda x: False,
            'AntisubPhase': lambda x: False,
            'FirstTorpedoPhase': lambda x:
                (x.level > 10) and (x.damaged < 3),
            'FirstShellingPhase': lambda x: x.damaged < 4,
            'SecondShellingPhase': lambda x:
                (x.get_range() >= 3) and (x.damaged < 4),
            'SecondTorpedoPhase': lambda x:
                (x.damaged < 3) and (x.get_final_status('torpedo') > 0),
            'SecondMissilePhase': lambda x: False,
            'NightPhase': lambda x: x.damaged < 3,
        }  # 可行动标准

        from src.wsgr.formulas import NormalAtk
        self.normal_atk = NormalAtk
        self.anti_sub_atk = None
        self.night_atk = None

    def __eq__(self, other):
        return self.cid == other.cid and \
               self.loc == other.loc and \
               self.side == other.side

    def __ne__(self, other):
        return self.cid != other.cid or \
               self.loc != other.loc or \
               self.side != other.side

    def __repr__(self):
        damage = ['未定义', '正常', '中破', '大破', '撤退']
        return f"{type(self).__name__}: {self.status['name']}, 状态: {damage[self.damaged]}"

    def set_master(self, master):
        self.master = master

    def get_form(self):
        """阵型
        1: 单纵; 2: 复纵; 3: 轮形; 4: 梯形; 5: 单横"""
        return self.master.form

    def get_recon_flag(self):
        """索敌"""
        if self.timer.recon_flag is None:
            raise ValueError('Recon flag not defined!')
        if self.side:
            return self.timer.recon_flag
        else:
            return False

    def get_dir_flag(self):
        """航向, 优同反劣分别为1-4"""
        if self.timer.direction_flag is None:
            raise ValueError('Direction flag not defined!')
        if self.side:
            return self.timer.direction_flag
        else:
            return 5 - self.timer.direction_flag

    def get_air_con_flag(self):
        """制空结果, 从空确到空丧分别为1-5"""
        if self.timer.air_con_flag is None:
            raise ValueError('Air control flag not defined!')
        if self.side:
            return self.timer.air_con_flag
        else:
            return 6 - self.timer.air_con_flag

    def set_cid(self, cid):
        """设置舰船编号"""
        self.cid = cid

    def set_side(self, side):
        """敌我判断"""
        self.side = side

    def set_loc(self, loc):
        """设置舰船站位"""
        self.loc = loc

    def set_level(self, level):
        """设置舰船等级"""
        self.level = level

    def set_affection(self, affection):
        """设置舰船好感度"""
        self.affection = affection

    def get_affection(self):
        """获取舰船好感度"""
        if self.side == 0:
            return 50
        if self.cid[0] != 1:
            return 50
        return self.affection

    def add_skill(self, skill):
        """设置舰船技能(未实例化)"""
        self._skill.extend(skill)

    def init_skill(self, friend, enemy):
        """舰船技能实例化，并结算常驻面板技能"""
        self.skill = []
        for skill in self._skill[:]:
            tmp_skill = skill(self.timer, self)
            if tmp_skill.is_common():  # 常驻面板技能，仅初始化一次，后续不再处理
                tmp_skill.activate(friend, enemy)
                self._skill.remove(skill)
            else:
                self.skill.append(tmp_skill)

        # 装备技能
        for tmp_equip in self.equipment:
            e_skill, e_value = tmp_equip.get_skill()
            if len(e_skill):
                assert len(e_skill) == 1
                tmp_skill = e_skill[0](self.timer, self, e_value)
                self.skill.append(tmp_skill)

    def get_raw_skill(self):
        """获取技能，让巴尔可调用"""
        return self._skill[:]

    def run_prepare_skill(self, friend, enemy):
        """结算准备阶段技能，让巴尔技能可用"""
        for tmp_skill in self.skill:
            if tmp_skill.is_prep() and \
                    tmp_skill.is_active(friend, enemy):
                tmp_skill.activate(friend, enemy)

    def run_raw_prepare_skill(self, friend, enemy):
        """结算准备阶段技能，让巴尔技能不可用"""
        for tmp_skill in self.skill:
            # 跳过让巴尔偷取技能
            if tmp_skill.request is None and \
                    tmp_skill.request is None and \
                    tmp_skill.buff is None:
                continue

            if tmp_skill.is_prep() and \
                    tmp_skill.is_active(friend, enemy):
                tmp_skill.activate(friend, enemy)

    def run_normal_skill(self, friend, enemy):
        """结算普通技能"""
        for tmp_skill in self.skill:
            if not tmp_skill.is_prep() and \
                    tmp_skill.is_active(friend, enemy):
                tmp_skill.activate(friend, enemy)

    def set_equipment(self, equipment):
        """设置舰船装备"""
        if isinstance(equipment, list):
            self.equipment = equipment
        else:
            self.equipment.append(equipment)

    def set_load(self, load):
        if isinstance(load, list):
            self.load = load
        else:
            raise AttributeError(f"'load' should be list, got {type(load)} instead.")

    def init_health(self):
        """初始化血量"""
        # standard_health 血量战损状态计算标准
        self.status['standard_health'] = self.status['total_health']
        for tmp_buff in self.common_buff:
            if tmp_buff.name == 'health':
                self.status['standard_health'] += tmp_buff.value
        self.status['standard_health'] += self.get_equip_status('health')
        self.status['health'] = self.status['standard_health']

    def set_status(self, name=None, value=None, status=None):
        """根据属性名称设置本体属性"""
        if status is None:
            if (name is not None) and (value is not None):
                self.status[name] = value
            else:
                raise ValueError("'name', 'value' and 'status' should not be all None!")
        else:
            if isinstance(status, dict):
                self.status = status
            else:
                raise AttributeError(f"'status' should be dict, got {type(status)} instead.")

    def get_status(self, name):
        """根据属性名称获取本体属性，包含常驻面板加成"""
        status = self.status.get(name, 0)
        if isinstance(status, str):  # 国籍、名称、tag等，直接返回
            return status

        scale_add = 0
        scale_mult = 1
        bias = 0
        for tmp_buff in self.common_buff:
            if tmp_buff.name == name:
                if tmp_buff.bias_or_weight == 0:
                    bias += tmp_buff.value
                elif tmp_buff.bias_or_weight == 1:
                    scale_add += tmp_buff.value
                elif tmp_buff.bias_or_weight == 2:
                    scale_mult *= (1 + tmp_buff.value)
                else:
                    pass
        status = status * (1 + scale_add) * scale_mult + bias
        return max(0, status)

    def get_equip_status(self, name, equiptype=None):
        """根据属性名称获取装备属性"""
        status = 0
        for tmp_equip in self.equipment:
            if (equiptype is None) or isinstance(tmp_equip, equiptype):
                status += tmp_equip.get_final_status(name)
        return status

    def get_final_status(self, name, equip=True):
        """根据属性名称获取属性总和"""
        buff_scale_1, buff_scale_2, buff_bias = self.get_buff(name)
        status = self.get_status(name) * (1 + buff_scale_1) * buff_scale_2

        if equip and name != 'speed':
            status += self.get_equip_status(name) * buff_scale_2

        status += buff_bias

        return max(0, status)

    def get_range(self):
        ship_range = self.status['range']

        for tmp_buff in self.common_buff:
            if tmp_buff.name == 'range' and tmp_buff.is_active():
                tmp_range = tmp_buff.value
                ship_range = max(ship_range, tmp_range)
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'range' and tmp_buff.is_active():
                tmp_range = tmp_buff.value
                ship_range = max(ship_range, tmp_range)
        for tmp_equip in self.equipment:
            equip_range = tmp_equip.get_range()
            ship_range = max(ship_range, equip_range)

        return ship_range

    def add_buff(self, buff):
        """添加增益"""
        buff.set_master(self)
        if buff.is_common():
            self.common_buff.append(buff)

        elif buff.is_active_buff():
            self.active_buff.append(buff)

        elif buff.is_event():
            self.timer.queue_append(buff)

        else:
            self.temper_buff.append(buff)

    def get_buff(self, name, *args, **kwargs):
        """根据增益名称获取全部属性增益"""
        scale_add = 0
        scale_mult = 1
        bias = 0
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == name and tmp_buff.is_active(*args, **kwargs):
                if tmp_buff.bias_or_weight == 0:
                    bias += tmp_buff.value
                elif tmp_buff.bias_or_weight == 1:
                    scale_add += tmp_buff.value
                elif tmp_buff.bias_or_weight == 2:
                    scale_mult *= (1 + tmp_buff.value)
                else:
                    pass
        return scale_add, scale_mult, bias  # 先scale后bias

    def get_atk_buff(self, name, atk, *args, **kwargs):
        """根据增益名称获取全部攻击系数增益(含攻击判断)"""
        scale_add = 0
        scale_mult = 1
        bias = 0
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == name and tmp_buff.is_active(atk=atk, *args, **kwargs):
                if tmp_buff.bias_or_weight == 0:
                    bias += tmp_buff.value
                elif tmp_buff.bias_or_weight == 1:
                    scale_add += tmp_buff.value
                elif tmp_buff.bias_or_weight == 2:
                    scale_mult *= (1 + tmp_buff.value)
                else:
                    pass
        return (1 + scale_add) * scale_mult - 1, bias  # 先scale后bias

    def atk_coef_process(self, atk, *args, **kwargs):
        for tmp_buff in self.temper_buff:
            if not tmp_buff.is_coef_process():
                continue
            if tmp_buff.is_active(atk=atk, *args, **kwargs):
                atk.set_coef({tmp_buff.name: tmp_buff.value})

    def get_special_buff(self, name, *args, **kwargs):
        """查询机制增益"""
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == name:
                if tmp_buff.is_active(*args, **kwargs):
                    tmp_buff.activate(*args, **kwargs)
                    return True
        return False

    def get_unique_effect(self, effect_type):
        if not isinstance(effect_type, list):
            effect_type = [effect_type]

        for tmp_buff in self.temper_buff:
            if tmp_buff.is_equip_effect():
                if tmp_buff.effect_type in effect_type:
                    return tmp_buff
        return None

    def get_final_damage_buff(self, atk):
        """根据攻击类型决定终伤加成"""
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'final_damage_buff' and \
                    tmp_buff.is_active(atk=atk):
                yield tmp_buff.value

    def get_final_damage_debuff(self, atk):
        """根据攻击类型决定终伤减伤加成"""
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'final_damage_debuff' and \
                    tmp_buff.is_active(atk=atk):
                yield tmp_buff.value

    def get_act_indicator(self):
        """判断舰船在指定阶段内能否行动"""
        # 跳过阶段，优先级最高
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'not_act_phase' and tmp_buff.is_active():
                return False

        # 可参与阶段
        # for tmp_buff in self.temper_buff:
        #     if tmp_buff.name == 'act_phase' and tmp_buff.is_active():
        #         return True

        # 默认行动模式
        phase_name = type(self.timer.phase).__name__
        return self.act_phase_indicator[phase_name](self)

    def raise_atk(self, target_fleet):
        """判断炮击战、夜战攻击类型(todo 夜战、航战)"""
        # 技能发动特殊攻击
        for tmp_buff in self.active_buff:
            if tmp_buff.is_active(atk=self.normal_atk, enemy=target_fleet):
                return tmp_buff.active_start(atk=self.normal_atk, enemy=target_fleet)

        # 技能优先攻击特定船型
        prior = self.get_prior_type_target(target_fleet)
        if prior is not None:
            atk = self.normal_atk(
                timer=self.timer,
                atk_body=self,
                def_list=prior,
            )
            return [atk]

        # 优先反潜
        elif self.anti_sub_atk is not None:
            def_list = target_fleet.get_atk_target(atk_type=self.anti_sub_atk)
            if len(def_list):
                atk = self.anti_sub_atk(
                    timer=self.timer,
                    atk_body=self,
                    def_list=def_list,
                )
                return [atk]

        # 常规攻击模式
        else:
            def_list = target_fleet.get_atk_target(atk_type=self.normal_atk)
            if not len(def_list):
                return []

            atk = self.normal_atk(
                timer=self.timer,
                atk_body=self,
                def_list=def_list,
            )
            return [atk]

    # def get_atk_type(self, target):  # 备用接口
    #     """判断攻击该对象时使用什么攻击类型"""
    #     pass

    def can_be_atk(self, atk):
        """判断舰船是否可被某攻击类型指定"""
        return self.damaged <= 3

    def get_prior_type_target(self, fleet, *args, **kwargs):
        """获取指定列表可被自身优先攻击船型的目标"""
        if isinstance(fleet, Fleet):
            fleet = fleet.ship
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'prior_type_target' and \
                    tmp_buff.is_active(*args, **kwargs):
                return tmp_buff.activate(fleet)

    def get_prior_loc_target(self, fleet, *args, **kwargs):
        """获取指定列表可被自身优先攻击站位的目标"""
        if isinstance(fleet, Fleet):
            fleet = fleet.ship
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'prior_loc_target' and \
                    tmp_buff.is_active(*args, **kwargs):
                return tmp_buff.activate(fleet)

    def atk_hit(self, name, atk, *args, **kwargs):
        """处理命中后、被命中后添加buff效果（含反击）"""
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == name and \
                    tmp_buff.is_active(atk=atk, *args, **kwargs):
                tmp_buff.activate(atk=atk, *args, **kwargs)

        if name == 'be_atk_hit':
            for tmp_buff in self.temper_buff:
                if tmp_buff.name == 'hit_back' and \
                        tmp_buff.is_active(atk=atk, *args, **kwargs):
                    return tmp_buff.activate(atk=atk, *args, **kwargs)

    def get_act_flag(self):
        phase_name = type(self.timer.phase).__name__
        return self.act_phase_flag[phase_name]

    def get_damage(self, damage):
        """受伤结算，过伤害保护，需要返回受伤与否"""
        standard_health = self.status['standard_health']

        # 敌方没有伤害保护，大破进击没有伤害保护
        if self.side == 0 or \
                not self.damage_protect or \
                self.damaged == 4:
            pass

        # 友方大破时受伤, 非大破进击
        elif self.damaged == 3:
            if self.status['health'] == 1:  # 剩余血量为1，强制miss
                damage = 0
            else:
                damage = np.ceil(self.status['health'] * 0.1)

        # 友方非大破状态下，受到足以大破的伤害
        elif self.status['health'] - damage < standard_health * 0.25:
            if self.status['health'] == standard_health:
                damage = np.ceil(standard_health * np.random.uniform(0.5, 0.75))
            else:
                damage = np.ceil(self.status['health'] - standard_health * 0.25)

        self.status['health'] -= int(damage)
        self.got_damage += int(damage)

        # 受伤状态结算
        if self.status['health'] <= 0:
            self.status['health'] = 0
            self.damaged = 4
        elif self.damaged < 3 and \
                self.status['health'] < standard_health * 0.25:
            self.damaged = 3
        elif self.damaged < 2 and \
                self.status['health'] < standard_health * 0.5:
            self.damaged = 2

        return damage

    def remove_during_buff(self):
        """去除攻击期间的临时buff"""
        # remove_list = []
        # for tmp_buff in self.temper_buff:
        #     if tmp_buff.is_during_buff():
        #         remove_list.append(tmp_buff)
        # for tmp_buff in remove_list:
        #     self.temper_buff.remove(tmp_buff)

        i = 0
        while i < len(self.temper_buff):
            tmp_buff = self.temper_buff[i]
            if tmp_buff.is_during_buff():
                self.temper_buff.remove(tmp_buff)
                continue
            else:
                i += 1

    def clear_buff(self):
        """清空临时buff"""
        self.temper_buff = []
        self.active_buff = []

    def reset(self):
        """初始化当前舰船"""
        self.clear_buff()
        supply = {'oil': 0, 'ammo': 0, 'steel': 0, 'almn': 0}

        # 统计补给耗油并补满
        supply['oil'] += np.ceil((1 - self.supply_oil) * self.status['supply_oil'])
        self.supply_oil = 1

        # 统计补给耗弹并补满
        supply['ammo'] += np.ceil((1 - self.supply_ammo) * self.status['supply_ammo'])
        self.supply_ammo = 1

        # 统计修理费用并恢复血量
        got_damage = self.status['standard_health'] - self.status['health']
        supply['oil'] += np.ceil(got_damage * self.status['repair_oil'])
        supply['steel'] += np.ceil(got_damage * self.status['repair_steel'])
        self.status['health'] = self.status['standard_health']

        # 统计铝耗并补满
        if len(self.load):
            for i in range(len(self.equipment)):
                tmp_equip = self.equipment[i]
                if isinstance(tmp_equip, (Plane, Missile, AntiMissile)):
                    supply_num = self.load[i] - tmp_equip.load
                    supply['almn'] += supply_num * tmp_equip.status['supply_almn']
                    tmp_equip.load = self.load[i]
        return supply


class LargeShip(Ship):
    """大型船总类"""

    def __init__(self, timer):
        super().__init__(timer)
        self.size = 3  # 船型


class MidShip(Ship):
    """中型船总类"""

    def __init__(self, timer):
        super().__init__(timer)
        self.size = 2  # 船型


class SmallShip(Ship):
    """小型船总类"""

    def __init__(self, timer):
        super().__init__(timer)
        self.size = 1  # 船型


class MainShip(Ship):
    """主力舰总类"""

    def __init__(self, timer):
        super().__init__(timer)
        self.function = 'main'


class CoverShip(Ship):
    """护卫舰总类"""

    def __init__(self, timer):
        super().__init__(timer)
        self.function = 'cover'


class Submarine(Ship):
    """水下单位"""

    def can_be_atk(self, atk):
        from src.wsgr.formulas import AntiSubAtk
        if isinstance(atk, AntiSubAtk):
            return True
        else:
            return False


class SS(Submarine, SmallShip, CoverShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'SS'

        self.act_phase_flag.update({
            'FirstTorpedoPhase': True,
            'FirstShellingPhase': False,
            'SecondShellingPhase': False,
        })


class SC(Submarine, SmallShip, CoverShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'SC'


class AntiSubShip(Ship):
    """反潜船"""
    def __init__(self, timer):
        super().__init__(timer)
        self.act_phase_flag.update({'AntisubPhase': True})

        self.act_phase_indicator.update({
            'AntisubPhase': lambda x:
                (x.get_form() == 5) and (x.damaged < 4),
        })

        from src.wsgr.formulas import AntiSubAtk
        self.anti_sub_atk = AntiSubAtk  # 反潜攻击


class Aircraft(Ship):
    """航系单位(所有可参与航空战攻击的单位)"""

    def __init__(self, timer):
        super().__init__(timer)
        self.flightparam = 0
        self.act_phase_flag.update({'AirPhase': True})
        self.act_phase_indicator.update({'AirPhase': lambda x: x.damaged < 3})

    def get_atk_plane(self):
        """检查攻击型飞机是否有载量"""
        for tmp_equip in self.equipment:
            if isinstance(tmp_equip, (Bomber, DiveBomber)):
                if tmp_equip.load > 0:
                    return True
        return False


class CV(Aircraft, LargeShip, MainShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'CV'
        self.flightparam = 5

        self.act_phase_flag.update({
            'AirPhase': True,
            'SecondTorpedoPhase': False,
            'NightPhase': False,
        })

        self.act_phase_indicator.update({
            'AirPhase': lambda x: x.damaged < 3,
            'FirstShellingPhase': lambda x:
                (x.damaged < 2) and (x.get_atk_plane()),
            'SecondShellingPhase': lambda x:
                (x.damaged < 2) and (x.get_atk_plane()) and (x.get_range() >= 3),
        })

        from src.wsgr.formulas import AirNormalAtk
        self.normal_atk = AirNormalAtk  # 炮击战航空攻击

    def get_act_indicator(self):
        # 跳过阶段，优先级最高
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'not_act_phase' and tmp_buff.is_active():
                return False

        # 可参与阶段
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'act_phase' and tmp_buff.is_active():
                return (self.damaged < 2) and (self.get_atk_plane())

        # 默认行动模式
        phase_name = type(self.timer.phase).__name__
        return self.act_phase_indicator[phase_name](self)


class CVL(Aircraft, AntiSubShip, MidShip, CoverShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'CVL'
        self.flightparam = 5

        self.act_phase_flag.update({
            'AirPhase': True,
            'AntisubPhase': True,
            'SecondTorpedoPhase': False,
            'NightPhase': False,
        })

        self.act_phase_indicator.update({
            'AirPhase': lambda x: x.damaged < 3,
            'AntisubPhase': lambda x:
                (x.damaged < 2) and (x.get_atk_plane()) and (x.get_form() == 5),
            'FirstShellingPhase': lambda x: x.damaged < 2,
            'SecondShellingPhase': lambda x:
                (x.damaged < 2) and (x.get_atk_plane()) and (x.get_range() >= 3),
        })

        from src.wsgr.formulas import AirNormalAtk
        self.normal_atk = AirNormalAtk  # 炮击战航空攻击
        from src.wsgr.formulas import AirAntiSubAtk
        self.anti_sub_atk = AirAntiSubAtk  # 反潜攻击

    def get_act_indicator(self):
        # 跳过阶段，优先级最高
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'not_act_phase' and tmp_buff.is_active():
                return False

        # 可参与阶段
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'act_phase' and tmp_buff.is_active():
                return (self.damaged < 2) and (self.get_atk_plane())

        # 默认行动模式
        phase_name = type(self.timer.phase).__name__
        return self.act_phase_indicator[phase_name](self)


class AV(Aircraft, LargeShip, MainShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'AV'
        self.flightparam = 5

        self.act_phase_flag.update({
            'AirPhase': True,
            'SecondTorpedoPhase': False,
            'NightPhase': False,
        })

        self.act_phase_indicator.update({
            'AirPhase': lambda x: x.damaged < 3,
            'FirstShellingPhase': lambda x:
                (x.damaged < 3) and (x.get_atk_plane()),
            'SecondShellingPhase': lambda x:
                (x.damaged < 3) and (x.get_atk_plane()) and (x.get_range() >= 3),
        })

        from src.wsgr.formulas import AirNormalAtk
        self.normal_atk = AirNormalAtk  # 炮击战航空攻击

    def get_act_indicator(self):
        # 跳过阶段，优先级最高
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'not_act_phase' and tmp_buff.is_active():
                return False

        # 可参与阶段
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'act_phase' and tmp_buff.is_active():
                return (self.damaged < 3) and (self.get_atk_plane())

        # 默认行动模式
        phase_name = type(self.timer.phase).__name__
        return self.act_phase_indicator[phase_name](self)


class BB(LargeShip, MainShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'BB'


class BC(LargeShip, MainShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'BC'


class BBV(Aircraft, LargeShip, MainShip):
    """航战"""
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'BBV'
        self.flightparam = 10

        self.act_phase_flag.update({
            'SecondTorpedoPhase': False,
        })

        self.act_phase_indicator.update({
            'SecondShellingPhase': lambda x:
                (x.get_range() >= 3) and (x.damaged < 3),
        })

        from src.wsgr.formulas import AirAntiSubAtk
        self.anti_sub_atk = AirAntiSubAtk  # 反潜攻击


class CAV(Aircraft, AntiSubShip, MidShip, CoverShip):
    """航巡"""
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'CAV'
        self.flightparam = 10


class CA(MidShip, CoverShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'CA'


class CL(AntiSubShip, MidShip, CoverShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'CL'


class CLT(MidShip, CoverShip):
    """雷巡"""
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'CLT'

        from src.wsgr.formulas import AntiSubAtk
        self.anti_sub_atk = AntiSubAtk  # 反潜攻击


class DD(AntiSubShip, SmallShip, CoverShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'DD'


class BM(SmallShip, CoverShip):
    pass


class AP(SmallShip, CoverShip):
    pass


class MissileShip(Ship):
    """导弹船"""

    def __init__(self, timer):
        super().__init__(timer)
        self.load = [0, 0, 0, 0]


class ASDG(MissileShip, SmallShip, MainShip):
    """导驱"""
    pass


class AADG(MissileShip, SmallShip, CoverShip):
    """防驱"""
    pass


class BBG(MissileShip, LargeShip, MainShip):
    """导战"""
    pass


class BG(MissileShip, LargeShip, MainShip):
    """大巡"""
    pass


class LandUnit(LargeShip, MainShip):
    """路基单位"""
    def can_be_atk(self, atk):
        from src.wsgr.formulas import TorpedoAtk  # , AntiSubAtk
        if isinstance(atk, TorpedoAtk):
            return False
        # elif isinstance(atk, AntiSubAtk):
        #     return False
        else:
            return True


class Elite(Aircraft, LargeShip, MainShip):
    """旗舰"""

    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'Elite'
        self.flightparam = 10

        self.act_phase_flag.update({
            'SecondTorpedoPhase': False,
        })


class Fortness(LandUnit, Aircraft):
    """要塞"""

    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'Fortness'
        self.flightparam = 10

        self.act_phase_flag.update({
            'SecondTorpedoPhase': False,
        })


class Airfield(LandUnit, Aircraft):
    """机场"""

    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'Airfield'
        self.flightparam = 10

        self.act_phase_flag.update({
            'SecondTorpedoPhase': False,
            'NightPhase': False,
        })

        self.act_phase_indicator.update({
            'AirPhase': lambda x: x.damaged < 3,
            'FirstShellingPhase': lambda x:
                (x.damaged < 3) and (x.get_atk_plane()),
            'SecondShellingPhase': lambda x:
                (x.damaged < 3) and (x.get_atk_plane()) and (x.get_range() >= 3),
        })

        from src.wsgr.formulas import AirNormalAtk
        self.normal_atk = AirNormalAtk  # 炮击战航空攻击


class Port(LandUnit):
    """港口"""
    pass


class Fleet(Time):
    def __init__(self, timer):
        super().__init__(timer)
        self.ship = []
        self.status = {}  # 舰队属性
        self.form = 0  # 阵型; 1: 单纵; 2: 复纵; 3: 轮形; 4: 梯形; 5: 单横
        self.side = 0  # 敌我识别; 1: 友方; 0: 敌方

    def __repr__(self):
        if self.side == 1:
            fleet_name = '友方舰队'
        else:
            fleet_name = '敌方舰队'
        form_list = ['单纵阵', '复纵阵', '轮形阵', '梯形阵', '单横阵']
        return f"{fleet_name}-{form_list[self.form - 1]}"

    def set_ship(self, shiplist):
        self.ship = shiplist

    def set_form(self, form):
        self.form = form

    def set_side(self, side):
        self.side = side
        for tmp_ship in self.ship:
            tmp_ship.set_side(side)

    def get_init_status(self):
        pass

    def get_avg_status(self, name):
        """获取平均数据"""
        if not len(self.ship):
            return 0

        status = 0
        for tmp_ship in self.ship:
            status += tmp_ship.get_final_status(name)
        status /= len(self.ship)
        return status

    def get_total_status(self, name):
        """获取属性总和"""
        if not len(self.ship):
            return 0

        status = 0
        for tmp_ship in self.ship:
            status += tmp_ship.get_final_status(name)
        return status

    def get_fleet_speed(self):
        """计算舰队航速"""
        main_type = (CV, CVL, AV, BB, BC, BBV, ASDG, AADG, BBG, BG,
                         Elite, Fortness, Airfield, Port)
        cover_type = (CA, CAV, CL, CLT, DD, BM, AP)

        # 存在水面舰
        if self.count(Submarine) != len(self.ship):
            main_speed = 0
            main_num = 0
            cover_speed = 0
            cover_num = 0
            for tmp_ship in self.ship:
                if isinstance(tmp_ship, main_type):
                    main_speed += tmp_ship.get_final_status('speed')
                    main_num += 1
                elif isinstance(tmp_ship, cover_type):
                    cover_speed += tmp_ship.get_final_status('speed')
                    cover_num += 1

            # debug
            if main_num + cover_num != len(self.ship):
                raise ValueError('Number of ship not consist')
            elif main_num == 0 and cover_num == 0:
                raise ValueError('Mainship and Covership are both 0')

            # 主力舰与护卫舰同时存在，航速向下取整并取较小值
            elif main_num != 0 and cover_num != 0:
                main_speed = np.floor(main_speed / main_num)
                cover_speed = np.floor(cover_speed / cover_num)
                return min(main_speed, cover_speed)

            # 否则不取整
            elif main_num != 0:
                return main_speed / main_num
            else:
                return cover_speed / cover_num

        # 只有水下舰
        else:
            speed = self.get_avg_status('speed')
            return np.floor(speed)

    def get_member_inphase(self):
        """确定舰队中参与当前阶段的成员(不论是否可以行动，以满足炮序计算需求)"""
        member = []
        for tmp_ship in self.ship:
            if tmp_ship.get_act_flag():
                member.append(tmp_ship)
        return member

    def get_act_member_inphase(self):
        """确定舰队中在当前阶段可行动的成员"""
        member = []
        for tmp_ship in self.ship:
            if tmp_ship.get_act_flag() and tmp_ship.get_act_indicator():
                member.append(tmp_ship)
        return member

    def get_atk_target(self, atk_type=None, atk_body=None):
        """确定舰队中可被指定攻击方式选中的成员"""
        target = []
        if atk_type is not None:
            for tmp_ship in self.ship:
                if tmp_ship.can_be_atk(atk_type):
                    target.append(tmp_ship)
        # elif atk_body is not None:
        #     for tmp_ship in self.ship:
        #         if tmp_ship in atk_body.get_target():
        #             target.append(tmp_ship)
        # else:
        #     raise ValueError('"atk_type" and "atk_body" should not be None at the same time!')
        return target

    def count(self, shiptype):
        c = 0
        for tmp_ship in self.ship:
            if isinstance(tmp_ship, shiptype):
                c += 1
        return c

    def clear_buff(self):
        for tmp_ship in self.ship:
            tmp_ship.clear_buff()
