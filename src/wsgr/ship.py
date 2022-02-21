# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 舰船类

# import sys
# sys.path.append(r'.\wsgr')

from .wsgrTimer import Time


class Ship(Time):
    """舰船总类"""

    def __init__(self):
        super().__init__()
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
            'armor': 0,  # 装甲
            'torpedo': 0,  # 鱼雷
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

        self.side = 0  # 敌我识别; 1: 友方; 0: 敌方
        self.loc = 0  # 站位, 1-6
        self.level = 110  # 等级
        self.affection = 200  # 好感
        self.damaged = 1  # 耐久状态, 1: 正常; 2: 中破; 3: 大破; 4: 撤退
        self.supply = 1.  # 补给状态
        self.common_buff = []  # 永久面板加成
        self.temper_buff = []  # 临时buff
        # self.target_list = []  # 优先攻击列表

    def __eq__(self, other):
        return self.cid == other.cid and \
               self.loc == other.loc and \
               self.side == other.side

    def __ne__(self, other):
        return self.cid != other.cid or \
               self.loc != other.loc or \
               self.side != other.side

    def __repr__(self):
        return f"Name: {self.status['name']}"

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
            tmp_skill = skill(self)
            if tmp_skill.is_common():  # 常驻面板技能，仅初始化一次，后续不再处理
                tmp_skill.activate(friend, enemy)
                self._skill.remove(skill)
            else:
                self.skill.append(tmp_skill)

    def set_equipment(self, equipment):
        """设置舰船装备"""
        if isinstance(equipment, list):
            self.equipment = equipment
        else:
            self.equipment.append(equipment)

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
        status = self.status.get(name, default=0)

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

    def get_equip_status(self, name):
        """根据属性名称获取装备属性"""
        status = 0
        for tmp_equip in self.equipment:
            status += tmp_equip.get_final_status(name)
        return status

    def get_final_status(self, name, equip=True):
        """根据属性名称获取属性总和"""
        buff_scale, buff_bias = self.get_buff(name)
        status = self.get_status(name) * (1 + buff_scale) + buff_bias

        if equip:
            status += self.get_equip_status(name)

        return max(0, status)

    def add_buff(self, buff):
        """添加增益"""
        buff.set_master(self)
        if buff.is_common():
            self.common_buff.append(buff)
        else:
            self.temper_buff.append(buff)
        if buff.is_event():
            self.timer.queue.append(buff)

    def get_buff(self, name):
        """根据增益名称获取全部属性增益"""
        scale_add = 0
        scale_mult = 1
        bias = 0
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == name and tmp_buff.is_active():
                if tmp_buff.bias_or_weight == 0:
                    bias += tmp_buff.value
                elif tmp_buff.bias_or_weight == 1:
                    scale_add += tmp_buff.value
                elif tmp_buff.bias_or_weight == 2:
                    scale_mult *= (1 + tmp_buff.value)
                else:
                    pass
        return (1 + scale_add) * scale_mult - 1, bias  # 先scale后bias

    def get_special_buff(self):
        """查询机制增益"""
        pass

    def act_in_phase(self):
        """判断舰船在指定阶段内能否行动"""
        pass

    def get_target(self):
        """判断指定阶段内可以攻击什么目标"""
        pass

    def get_prior_target(self):
        """获取指定阶段内优先攻击的目标"""
        pass

    def get_atk_type(self, target):
        """判断攻击该对象时使用什么攻击类型"""
        pass

    def can_be_atk(self, atk):
        """判断舰船是否可被某攻击类型指定"""
        pass

    def get_final_damage_buff(self, atk):
        """根据攻击类型决定终伤加成"""
        scale_mult = 1
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'final_damage_buff' \
                    and tmp_buff.is_active(atk=atk):
                scale_mult *= (1 + tmp_buff.value)
        return scale_mult

    def get_final_damage_debuff(self, atk):
        """根据攻击类型决定终伤减伤加成"""
        scale_mult = 1
        for tmp_buff in self.temper_buff:
            if tmp_buff.name == 'final_damage_debuff' \
                    and tmp_buff.is_active(atk=atk):
                scale_mult *= (1 + tmp_buff.value)
        return scale_mult

    def get_damage(self, damage):
        """受伤结算，过伤害保护，需要返回受伤与否"""
        return bool(damage)

    def clear_buff(self):
        """清空临时buff"""
        self.temper_buff = []

    def reset(self):
        """初始化当前舰船"""
        pass


class LargeShip(Ship):
    """大型船总类"""

    def __init__(self):
        super().__init__()
        self.type = 3  # 船型


class MidShip(Ship):
    """中型船总类"""

    def __init__(self):
        super().__init__()
        self.type = 2  # 船型


class SmallShip(Ship):
    """小型船总类"""

    def __init__(self):
        super().__init__()
        self.type = 1  # 船型


class MainShip(Ship):
    """主力舰总类"""

    def __init__(self):
        super().__init__()
        self.function = 'main'


class CoverShip(Ship):
    """护卫舰总类"""

    def __init__(self):
        super().__init__()
        self.function = 'cover'


class Aircraft(Ship):
    """航系单位(所有可参与航空战攻击的单位)"""

    def __init__(self):
        super().__init__()
        self.flightparam = 0
        self.load = []

    def set_load(self, load):
        if isinstance(load, list):
            self.load = load
        else:
            raise AttributeError(f"'load' should be list, got {type(load)} instead.")


class CV(Aircraft, LargeShip, MainShip):
    def __init__(self):
        super().__init__()
        self.type = 'CV'
        self.flightparam = 5

    def act_in_phase(self):
        return True

    def can_be_atk(self, atk):
        return True


class CVL(Aircraft, MidShip, CoverShip):
    def __init__(self):
        super().__init__()
        self.type = 'CVL'
        self.flightparam = 5


class AV(Aircraft, LargeShip, MainShip):
    def __init__(self):
        super().__init__()
        self.type = 'AV'
        self.flightparam = 5


class BB(LargeShip, MainShip):
    pass


class BC(LargeShip, MainShip):
    pass


class CA(MidShip, CoverShip):
    pass


class CL(MidShip, CoverShip):
    pass


class DD(SmallShip, CoverShip):
    pass


class Submarine(Ship):
    """水下单位"""
    pass


class SS(Submarine, SmallShip, CoverShip):
    pass


class SC(Submarine, SmallShip, CoverShip):
    pass


class Fleet(Time):
    def __init__(self):
        super().__init__()
        self.ship = []
        self.status = {}  # 舰队属性
        self.form = 0  # 阵型; 1: 单纵; 2: 复纵; 3: 轮形; 4: 梯形; 5: 单横
        self.side = 0  # 敌我识别; 1: 友方; 0: 敌方

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
            if tmp_ship.act_in_phase():
                member.append(tmp_ship)
        return member

    def get_target(self, atk_type=None, atk_body=None):
        """确定舰队中可被指定攻击方式选中的成员"""
        target = []
        if atk_type is not None:
            for tmp_ship in self.ship:
                if tmp_ship.can_be_atk(atk_type):
                    target.append(tmp_ship)
            return target
        elif atk_body is not None:
            for tmp_ship in self.ship:
                if tmp_ship in atk_body.get_target():
                    target.append(tmp_ship)
            return target

    def count(self, shiptype):
        c = 0
        for tmp_ship in self.ship:
            if isinstance(tmp_ship, shiptype):
                c += 1
        return c


if __name__ == "__main__":
    pass
