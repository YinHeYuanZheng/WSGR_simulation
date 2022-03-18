# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 舰船类

import numpy as np
from src.wsgr.wsgrTimer import Time
from src.wsgr.equipment import *
# import src.wsgr.formulas as rform


class Ship(Time):
    """舰船总类"""

    def __init__(self, timer):
        super().__init__(timer)
        self.master = None
        self.cid = 0  # 编号
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
        }

        self._skill = []  # 技能(未实例化)
        self.skill = []  # 技能
        self.equipment = []  # 装备
        self.load = []

        self.side = 0  # 敌我识别; 1: 友方; 0: 敌方
        self.loc = 0  # 站位, 1-6
        self.level = 110  # 等级
        self.affection = 200  # 好感
        self.damaged = 1  # 耐久状态, 1: 正常; 2: 中破; 3: 大破; 4: 撤退
        self.damage_protect = True  # 耐久保护，大破进击时消失
        self.supply = 1.  # 补给状态
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
            'AirPhase': lambda: False,
            'FirstMissilePhase': lambda: False,
            'AntisubPhase': lambda: False,
            'FirstTorpedoPhase': lambda: False,
            'FirstShellingPhase': lambda: self.damaged < 4,
            'SecondShellingPhase': lambda:
                (self.get_range() >= 3) and (self.damaged < 4),
            'SecondTorpedoPhase': lambda:
                (self.damaged < 3) and (self.get_final_status('torpedo') > 0),
            'SecondMissilePhase': lambda: False,
            'NightPhase': lambda: self.damaged < 3,
        }  # 可行动标准

        from src.wsgr.formulas import NormalAtk
        self.normal_atk = NormalAtk
        self.special_atk = None

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
        return self.master.form

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

    def add_skill(self, skill):
        """设置舰船技能(未实例化)"""
        self._skill.extend(skill)

    def init_skill(self, friend, enemy):
        """舰船技能实例化"""
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
            if tmp_buff.name == name and tmp_buff.is_active():
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
        buff_scale, buff_bias = self.get_buff(name)
        status = self.get_status(name) * (1 + buff_scale) + buff_bias

        if equip:
            status += self.get_equip_status(name)

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

    def get_unique_effect(self, effect_type):
        if not isinstance(effect_type, list):
            effect_type = [effect_type]

        for tmp_buff in self.temper_buff:
            if tmp_buff.is_equip_effect():
                if tmp_buff.effect_type in effect_type:
                    return tmp_buff
        return None

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
        return (1 + scale_add) * scale_mult - 1, bias  # 先scale后bias

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

    def atk_hit(self, name, atk, *args, **kwargs):
        """处理命中后、被命中后添加buff效果（不处理反击）"""
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == name and \
                    tmp_buff.is_active(atk=atk, *args, **kwargs):
                tmp_buff.activate(atk=atk, *args, **kwargs)

    def get_act_flag(self):
        phase_name = type(self.timer.phase).__name__
        return self.act_phase_flag[phase_name]

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
        return self.act_phase_indicator[phase_name]()

    def raise_atk(self, target_fleet):
        """判断炮击战、夜战攻击类型"""
        # 技能发动特殊攻击
        for tmp_buff in self.active_buff:
            if tmp_buff.is_active():
                return tmp_buff.active_start(atk=self.normal_atk, enemy=target_fleet)

        # 技能优先攻击特定船型
        def_list = target_fleet.get_atk_target(atk_type=self.normal_atk)
        prior = self.get_prior_type_target(def_list)
        if prior is not None:
            assert not isinstance(prior, list)
            atk = self.normal_atk(
                timer=self.timer,
                atk_body=self,
                target=prior,
                def_list=def_list,
            )
            atk.changeable = False
            return [atk]

        # 常规攻击模式
        else:
            atk = self.normal_atk(
                timer=self.timer,
                atk_body=self,
                def_list=def_list,
            )
            return [atk]

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

    def get_atk_type(self, target):
        """判断攻击该对象时使用什么攻击类型"""
        pass

    def can_be_atk(self, atk):
        """判断舰船是否可被某攻击类型指定"""
        return self.damaged <= 3

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

        self.status['health'] -= damage
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

    def clear_buff(self):
        """清空临时buff"""
        self.temper_buff = []

    def reset(self):
        """初始化当前舰船"""
        pass


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


class Aircraft(Ship):
    """航系单位(所有可参与航空战攻击的单位)"""

    def __init__(self, timer):
        super().__init__(timer)
        self.flightparam = 0

    def get_plane(self):
        for tmp_equip in self.equipment:
            if isinstance(tmp_equip, (Fighter, Bomber, DiveBomber)):
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
            'SecondTorpedoPhase': False
        })

        self.act_phase_indicator.update({
            'AirPhase': lambda: self.damaged < 3,
            'FirstShellingPhase': lambda: self.damaged < 2,
            'SecondShellingPhase': lambda:
                (self.damaged < 2) and (self.get_range() >= 3),
            'NightPhase': lambda: False,
        })

    def get_act_indicator(self):
        # 跳过阶段，优先级最高
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'not_act_phase' and tmp_buff.is_active():
                return False

        # 可参与阶段
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'act_phase' and tmp_buff.is_active():
                return self.damaged < 2

        # 默认行动模式
        phase_name = type(self.timer.phase).__name__
        return self.act_phase_indicator[phase_name]()


class CVL(Aircraft, MidShip, CoverShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'CVL'
        self.flightparam = 5

        self.act_phase_flag.update({
            'AirPhase': True,
            'AntisubPhase': True,
            'SecondTorpedoPhase': False
        })

        self.act_phase_indicator.update({
            'AirPhase': lambda: self.damaged < 3,
            'AntisubPhase': lambda:
                (self.damaged < 2) and self.get_atk_plane(),
            'FirstShellingPhase': lambda: self.damaged < 2,
            'SecondShellingPhase': lambda:
                (self.damaged < 2) and (self.get_range() >= 3),
            'NightPhase': lambda: False,
        })

    def get_act_indicator(self):
        # 跳过阶段，优先级最高
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'not_act_phase' and tmp_buff.is_active():
                return False

        # 可参与阶段
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'act_phase' and tmp_buff.is_active():
                return self.damaged < 2

        # 默认行动模式
        phase_name = type(self.timer.phase).__name__
        return self.act_phase_indicator[phase_name]()

    def get_atk_plane(self):
        for tmp_equip in self.equipment:
            if isinstance(tmp_equip, (Bomber, DiveBomber)):
                if tmp_equip.load > 0:
                    return True
        return False


class AV(Aircraft, LargeShip, MainShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'AV'
        self.flightparam = 5

        self.act_phase_flag.update({
            'AirPhase': True,
            'SecondTorpedoPhase': False
        })

        self.act_phase_indicator.update({
            'AirPhase': lambda: self.damaged < 3,
            'FirstShellingPhase': lambda: self.damaged < 3,
            'SecondShellingPhase': lambda:
                (self.damaged < 3) and (self.get_range() >= 3),
            'NightPhase': lambda: False,
        })

    def get_act_indicator(self):
        # 跳过阶段，优先级最高
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'not_act_phase' and tmp_buff.is_active():
                return False

        # 可参与阶段
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'act_phase' and tmp_buff.is_active():
                return self.damaged < 3

        # 默认行动模式
        phase_name = type(self.timer.phase).__name__
        return self.act_phase_indicator[phase_name]()


class BB(LargeShip, MainShip):
    pass


class BC(LargeShip, MainShip):
    pass


class BBV(Aircraft, LargeShip, MainShip):
    def __init__(self, timer):
        super().__init__(timer)
        self.type = 'BBV'
        self.flightparam = 10


class CA(MidShip, CoverShip):
    pass


class CL(MidShip, CoverShip):
    pass


class DD(SmallShip, CoverShip):
    pass


class Submarine(Ship):
    """水下单位"""

    def can_be_atk(self, atk):
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

        self.act_phase_indicator.update({
            'FirstTorpedoPhase': lambda: (self.level > 10) and (self.damaged < 3),
            'FirstShellingPhase': lambda: False,
            'SecondShellingPhase': lambda: False,
        })


class SC(Submarine, SmallShip, CoverShip):
    pass


class LandUnit(LargeShip, MainShip):
    """路基单位"""
    pass


class Elite(Aircraft, LargeShip, MainShip):
    """旗舰"""

    def __init__(self, timer):
        super().__init__(timer)
        self.flightparam = 10


class Fortness(LandUnit, Aircraft):
    """要塞"""

    def __init__(self, timer):
        super().__init__(timer)
        self.flightparam = 10


class Airfield(LandUnit, Aircraft):
    """机场"""

    def __init__(self, timer):
        super().__init__(timer)
        self.flightparam = 10


class Port(LandUnit):
    """港口"""
    pass


class MissileShip(Ship):
    """导弹船"""
    pass


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

    def get_status(self):
        pass

    def get_member_inphase(self):
        """确定舰队中参与当前阶段的成员"""
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
