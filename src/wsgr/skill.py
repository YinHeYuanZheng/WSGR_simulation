# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 技能类

import numpy as np
import copy

from src.wsgr.wsgrTimer import Time
from src.wsgr.ship import Fleet, Ship


class Skill(Time):
    def __init__(self, timer, master):
        """
        :param timer: src.wsgr.wsgrTimer.timer
        :param master: src.wsgr.ship.Ship
        """
        super().__init__(timer)
        self.master = master

        self.request = None  # list of Request, not initialised
        self.target = None  # Target
        self.buff = None  # list of Buff

    def is_active(self, friend, enemy):
        """技能是否满足发动条件, 子类可根据需要重新定义"""
        if self.request is None:
            return True
        else:
            return bool(self.request[0](self.timer, self.master, friend, enemy))

    def activate(self, friend, enemy):
        """技能生效时, 给所有满足条件的目标套上所有buff"""
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_buff = copy.copy(tmp_buff)
                tmp_target.add_buff(tmp_buff)

    def is_common(self):
        return False

    def is_prep(self):
        return False

    def is_end_skill(self):
        return False

    # def change_master(self, master):
    #     """让巴尔技能调用，更换技能master"""
    #     self.master = master
    #
    #     if self.request is not None:
    #         for tmp_request in self.request:
    #             tmp_request.change_master(master)
    #
    #     if self.target is not None:
    #         self.target.change_master(master)

    def change_rate(self, rate):
        """让巴尔技能调用，更改发动概率"""
        if self.buff is None:
            raise ValueError(f'{self.master.status["name"]}.buff should not be None!')
        for tmp_buff in self.buff:
            tmp_buff.change_rate(rate)


class CommonSkill(Skill):
    """仅包含常驻面板加成的技能"""
    def is_common(self):
        return True


class PrepSkill(Skill):
    """影响队友航速、索敌的技能，需要在buff阶段前结算"""
    def is_prep(self):
        return True


class EndSkill(Skill):
    """结束阶段技能(女灶神)"""
    def is_end_skill(self):
        return True


class EquipSkill(Skill):
    """装备携带特效"""

    def __init__(self, timer, master, value: list):
        """
        :param master: 装备携带者, Ship
        :param value: 技能数值，可以为空，数据库内以','分隔，读取后为list
        """
        super().__init__(timer, master)
        self.value = value

    # def activate(self, friend, enemy):  # 特效叠加判定目前已转移到ship内
    #     """技能生效时, 给所有满足条件的目标套上所有buff"""
    #     target = self.target.get_target(friend, enemy)
    #     for tmp_target in target:
    #         for tmp_buff in self.buff[:]:
    #             tmp_buff = copy.copy(tmp_buff)
    #             buff_type = tmp_buff.effect_type
    #
    #             # 2类不叠加(2类为舰船技能，标注为多个单位携带此技能不重复生效)
    #             # 注意2类每个buff标识数字各不相同
    #             if 2 <= buff_type < 3:
    #                 type2 = tmp_target.get_unique_effect(effect_type=buff_type)
    #
    #                 # 有2类特效，跳过
    #                 if type2 is not None:
    #                     continue
    #
    #             # 3和4类不叠加
    #             elif buff_type in [3, 4]:
    #                 type34 = tmp_target.get_unique_effect(effect_type=buff_type)
    #
    #                 # 特效类型相同，取最高值
    #                 if type34 is not None:
    #                     value1 = tmp_buff.value
    #                     value2 = type34.value
    #                     type34.set_value(max(value1, value2))
    #                     continue
    #
    #                 # 特效类型不同，跳过(现版本已取消)
    #                 # elif type34.effect_type != buff_type:
    #                 #     continue
    #
    #             tmp_target.add_buff(tmp_buff)


class Strategy(Skill):
    """战术"""

    def __init__(self, timer, master, level):
        super().__init__(timer, master)
        self.stid = '000'  # 战术编号
        self.level = level


class FleetStrategy(Strategy):
    """光环战术"""

    def activate(self, friend, enemy):
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            buff = copy.copy(self.buff[0])
            tmp_target.add_strategy_buff(buff, self.stid)


class SelfStrategy(Strategy):
    """单体战术"""

    def activate(self, *args, **kwargs):
        buff = copy.copy(self.buff[0])
        self.master.add_strategy_buff(buff, self.stid)


class Request(Time):
    """技能发动条件"""

    def __init__(self, timer, master, friend, enemy):
        super().__init__(timer)
        self.master = master
        self.friend = friend
        self.enemy = enemy

    def __bool__(self):
        pass

    # def change_master(self, master):
    #     """让巴尔技能调用，更换技能master"""
    #     self.master = master


class ATKRequest(Time):
    """判断攻击类型、攻击目标等"""

    def __init__(self, timer, atk):
        super().__init__(timer)
        self.atk = atk

    def __bool__(self):
        pass


class Target:
    def __init__(self, side):
        self.side = side  # 敌我识别; 1: 友方; 0: 敌方

    def get_target(self, friend, enemy):
        """
        无任何条件，仅根据side返回舰队全体
        :param friend: class Fleet
        :param enemy: class Fleet
        :return: list
        """
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side:
            return friend
        else:
            return enemy

    # def change_master(self, master):
    #     pass


class CombinedTarget(Target):
    """多个Target类组合筛选"""

    def __init__(self, side, target_list: list):
        """
        :param target_list: list of Target, 筛选将按照列表内顺序依次进行
        """
        super().__init__(side)
        # 检查列表内target的side是否与自身一致
        for target in target_list:
            if target.side != self.side:
                raise ValueError('"side" of one CombinedTarget should be the same!')
        self.target_list = target_list

    def get_target(self, friend, enemy):
        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        for tmp_target in self.target_list:
            if self.side == 1:
                fleet = tmp_target.get_target(fleet, None)
            else:
                fleet = tmp_target.get_target(None, fleet)

        return fleet


class SelfTarget(Target):
    """自身buff"""
    def __init__(self, master, side=1):
        super().__init__(side)
        self.master = master

    def get_target(self, friend, enemy):
        return [self.master]

    # def change_master(self, master):
    #     """让巴尔技能调用，更换技能master"""
    #     self.master = master


class TypeTarget(Target):
    """指定船型的目标"""
    def __init__(self, side, shiptype):
        """
        :praram shiptype: tuple or class Ship
        """
        super().__init__(side)
        self.shiptype = shiptype

    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = [ship for ship in fleet if isinstance(ship, self.shiptype)]
        return target


class AntiTypeTarget(TypeTarget):
    """指定船型以外的目标"""
    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = [ship for ship in fleet if not isinstance(ship, self.shiptype)]
        return target


class RandomTarget(Target):
    """随机选择n个目标"""
    def __init__(self, side, num):
        super().__init__(side)
        self.num = num

    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        if len(fleet) > self.num:
            target = np.random.choice(fleet, self.num, replace=False)
        else:
            target = fleet
        return target


class RandomTypeTarget(TypeTarget):
    """指定船型内随机选择n个目标"""
    def __init__(self, side, shiptype, num=1):
        super().__init__(side, shiptype)
        self.num = num

    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = [ship for ship in fleet if isinstance(ship, self.shiptype)]
        if len(target) > self.num:
            target = np.random.choice(target, self.num, replace=False)
        return target


class OrderedTypeTarget(TypeTarget):
    """按照指定船型的顺序+站位顺序选择目标"""
    def __init__(self, shiptype, side=0):
        super().__init__(side, shiptype)

    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = []
        for tmp_type in self.shiptype:
            target.extend([ship for ship in fleet if isinstance(ship, tmp_type)])
        return target


class CidTarget(Target):
    """指定cid的目标"""
    def __init__(self, side, cid_list: list):
        super().__init__(side)
        self.cid_list = cid_list

    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = [ship for ship in fleet if ship.cid in self.cid_list]
        return target


class LocTarget(Target):
    """指定站位的目标"""
    def __init__(self, side, loc: list):
        """
        :param loc: list, 站位, 数值范围1-6
        """
        super().__init__(side)
        self.loc = loc

    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = [ship for ship in fleet
                  if ship.loc in self.loc]
        return target


class NearestLocTarget(Target):
    def __init__(self, side, master, radius, direction,
                 master_include=False, expand=False, shiptype=Ship):
        """
        距离最近的(上方/下方/相邻)，可指定船型，可以检索不完整队列
        :param side:
        :param master: 技能所有者
        :param radius: 相邻半径
        :param direction: 相邻方向, up, down, near
        :param master_include: 技能是否包含所有者, default: False
        :param expand: 是否可顺延, default: False
        :param shiptype: 船型, default: all types i.e.(Ship,)
        """
        super().__init__(side)
        self.master = master
        self.radius = radius
        self.direction = direction
        self.master_include = master_include
        self.expand = expand
        self.shiptype = shiptype

    # def change_master(self, master):
    #     """让巴尔技能调用，更换技能master"""
    #     self.master = master

    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = []
        if not len(fleet):
            return target

        # 获取上方满足条件的目标
        if self.direction == 'up' or self.direction == 'near':
            target.extend(self.get_up_target(fleet))

        # 技能涉及自身时增加自身
        if self.master_include:
            target.append(self.master)

        # 获取下方满足条件的目标
        if self.direction == 'down' or self.direction == 'near':
            target.extend(self.get_down_target(fleet))

        return target

    def get_up_target(self, fleet):
        if isinstance(fleet, Fleet):
            fleet = fleet.ship

        target = []
        for tmp_ship in fleet[::-1]:
            # 跳过站位在master后方的
            if tmp_ship.loc >= self.master.loc:
                continue

            # 对于超过指定距离的船，如果不可顺延，则直接结束循环
            elif self.master.loc - tmp_ship.loc > self.radius \
                    and not self.expand:
                break

            # 在指定距离内，或可顺延
            if isinstance(tmp_ship, self.shiptype):
                target.append(tmp_ship)

            if len(target) >= self.radius:
                break

        target.sort(key=lambda x: x.loc)
        return target

    def get_down_target(self, fleet):
        if isinstance(fleet, Fleet):
            fleet = fleet.ship

        target = []
        for tmp_ship in fleet:
            # 跳过站位在master前方的
            if tmp_ship.loc <= self.master.loc:
                continue

            # 对于超过指定距离的船，如果不可顺延，则直接结束循环
            elif tmp_ship.loc - self.master.loc > self.radius \
                    and not self.expand:
                break

            # 在指定距离内，或可顺延
            if isinstance(tmp_ship, self.shiptype):
                target.append(tmp_ship)

            if len(target) >= self.radius:
                break

        target.sort(key=lambda x: x.loc)
        return target


class CountryTarget(Target):
    """指定国籍的目标(可指定多个国籍)"""
    def __init__(self, side, country: str):
        super().__init__(side)
        self.country = country

    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = [ship for ship in fleet
                  if ship.status['country'] in self.country]
        return target


class TagTarget(Target):
    """指定标签的目标(可指定国籍等字符串属性)"""

    def __init__(self, side, tag, tag_name='tag'):
        super().__init__(side)
        self.tag = tag
        self.tag_name = tag_name

    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = [ship for ship in fleet
                  if ship.status[self.tag_name] == self.tag]
        return target


class NotTagTarget(TagTarget):
    """非指定标签的目标(可指定国籍等字符串属性)"""
    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        target = [ship for ship in fleet
                  if ship.status[self.tag_name] != self.tag]
        return target


class StatusTarget(Target):
    """指定属性的目标(字符串属性除外)"""

    def __init__(self, side, status_name, fun, value):
        """
        指定属性与给定的value比较，返回符合fun定义的目标
        :param status_name: str
        :param fun: str; 'eq': =, 'ge': >=, 'gt': >, 'le': <=, 'lt': <
        :param value:
        """
        super().__init__(side)
        self.status_name = status_name
        self.fun = fun
        self.value = value

    def get_target(self, friend, enemy):
        if isinstance(friend, Fleet):
            friend = friend.ship
        if isinstance(enemy, Fleet):
            enemy = enemy.ship

        if self.side == 1:
            fleet = friend
        else:
            fleet = enemy

        if self.fun == 'eq':
            target = [ship for ship in fleet
                      if ship.get_final_status(self.status_name) == self.value]
        elif self.fun == 'ge':
            target = [ship for ship in fleet
                      if ship.get_final_status(self.status_name) >= self.value]
        elif self.fun == 'gt':
            target = [ship for ship in fleet
                      if ship.get_final_status(self.status_name) > self.value]
        elif self.fun == 'le':
            target = [ship for ship in fleet
                      if ship.get_final_status(self.status_name) <= self.value]
        elif self.fun == 'lt':
            target = [ship for ship in fleet
                      if ship.get_final_status(self.status_name) < self.value]
        else:
            raise ValueError()
        return target


class EquipTarget(Target):
    """装备"""
    def __init__(self, side, target, equiptype=None):
        super().__init__(side)
        self.target = target  # Target, 描述目标装备的携带者
        self.equiptype = equiptype  # tuple, 目标装备类型

    def get_target(self, friend, enemy):
        """返回目标对象所携带的满足条件的装备对象"""
        ship_target = self.target.get_target(friend, enemy)
        equip_target = []
        for tmp_ship in ship_target:
            for tmp_equip in tmp_ship.equipment:
                if self.equiptype is None or \
                        isinstance(tmp_equip, self.equiptype):
                    equip_target.append(tmp_equip)
        return equip_target


class Buff(Time):
    """增益总类"""
    def __init__(self, timer, name, phase, bias_or_weight=3, rate=1):
        super().__init__(timer)
        self.master = None
        self.name = name  # 检索用名称
        self.phase = phase  # 发动阶段, tuple

        # flag, 0: bias; 1: weight add; 2: weight mult; 3: not available
        self.bias_or_weight = bias_or_weight
        self.rate = rate

    def __repr__(self):
        return f"{self.name}"

    def set_master(self, master):
        self.master = master

    def change_rate(self, rate):
        self.rate = rate

    def is_common(self):
        return False

    def is_event(self):
        return False

    def is_active_buff(self):
        return False

    def is_unique_effect(self):
        return False

    def is_coef_process(self):
        return False

    def is_during_buff(self):
        return False

    def is_active(self, *args, **kwargs):
        """技能是否满足发动阶段"""
        self.change_value(*args, **kwargs)
        return self.rate_verify() and \
               isinstance(self.timer.phase, self.phase)

    def change_value(self, *args, **kwargs):
        """动态修改技能数值时调用"""
        pass

    def rate_verify(self):
        if self.rate == 1:
            return True
        else:
            tmp_rate = np.random.random()
            return tmp_rate <= self.rate


class StatusBuff(Buff):
    """属性增益"""
    def __init__(self, timer, name, phase, value, bias_or_weight, rate=1):
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.value = value

    def __repr__(self):
        return f"{self.name}: {self.value}"


class CommonBuff(StatusBuff):
    """常驻增益(通常直接显示在面板上)"""
    def is_common(self):
        return True

    def is_active(self, *args, **kwargs):
        return True


class CoeffBuff(Buff):
    """系数增益"""
    def __init__(self, timer, name, phase, value, bias_or_weight, rate=1):
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.value = value

    def __repr__(self):
        return f"{self.name}: {self.value}"


class UniqueEffect(Buff):
    """唯一特效"""

    def __init__(self, timer, effect_type, name, phase, value, bias_or_weight, rate=1):
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.value = value
        self.effect_type = effect_type

    def __repr__(self):
        return f"{self.name}: {self.value}(唯一特效{self.effect_type})"

    def is_unique_effect(self):
        return True

    def set_value(self, value):
        self.value = value


class EquipEffect(UniqueEffect):
    """装备自带特效"""

    def __repr__(self):
        return f"{self.name}: {self.value}(装备特效{self.effect_type})"


class AtkBuff(CoeffBuff):
    """攻击公式增益"""

    def __init__(self, timer, name, phase, value, bias_or_weight,
                 atk_request=None, rate=1):
        """
        :param atk_request: ATKRequest, 攻击判断(攻击者、被攻击者、攻击类型)
        """
        super().__init__(timer, name, phase, value, bias_or_weight, rate)
        self.atk_request = atk_request

    def is_active(self, *args, **kwargs):
        self.change_value(*args, **kwargs)
        if self.atk_request is None:
            return isinstance(self.timer.phase, self.phase) and \
                   self.rate_verify()

        try:
            atk = kwargs['atk']
        except:
            atk = args[0]

        return isinstance(self.timer.phase, self.phase) and \
               bool(self.atk_request[0](self.timer, atk)) and \
               self.rate_verify()


class DuringAtkBuff(CoeffBuff):
    """某一攻击结算期间有效"""
    def __init__(self, timer, name, phase, bias_or_weight,
                 value=None, rate=1):
        super().__init__(timer, name, phase, value, bias_or_weight, rate)

    def __repr__(self):
        if self.value is None:
            return f"{self.name}(temporal)"
        else:
            return f"{self.name}(temporal): {self.value}"

    def is_during_buff(self):
        return True


class AtkHitBuff(Buff):
    """攻击时、命中后效果"""
    def __init__(self, timer, name, phase, buff, side,
                 atk_request=None, bias_or_weight=3, rate=1):
        """
        :param name:    'atk_hit'       自身攻击命中并造成伤害后
                        'atk_be_hit'    自身被攻击命中并造成伤害后
                        'give_atk'      自身攻击时
                        'get_atk'       自身被攻击时
        :param buff: 施加效果内容
        :param side: 给谁加, 0: 敌方; 1: 友方
        :param atk_request: ATKRequest, 攻击判断(攻击者、被攻击者、攻击类型)
        """
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.buff = buff
        self.side = side
        self.atk_request = atk_request

    def is_active(self, atk, *args, **kwargs):
        if self.atk_request is None:
            return isinstance(self.timer.phase, self.phase) and \
                   self.rate_verify()

        return isinstance(self.timer.phase, self.phase) and \
               bool(self.atk_request[0](self.timer, atk)) and \
               self.rate_verify()

    def activate(self, atk, *args, **kwargs):
        if (self.name in ['atk_hit', 'give_atk'] and self.side == 1) or \
                (self.name in ['atk_be_hit', 'get_atk'] and self.side == 0):
            target = atk.atk_body
        else:
            target = atk.target

        for tmp_buff in self.buff[:]:
            tmp_buff = copy.copy(tmp_buff)
            target.add_buff(tmp_buff)


class AtkCoefProcess(AtkBuff):
    """直接修改攻击属性(船损、航向、制空系数等)"""
    def __init__(self, timer, name, phase, value,
                 bias_or_weight=3, atk_request=None, rate=1):
        super().__init__(timer, name, phase, value, bias_or_weight, atk_request, rate)

    def is_coef_process(self):
        return True


class FinalDamageBuff(AtkBuff):
    """终伤系数, 乘算, 需要判断攻击类型"""
    def __init__(self, timer, name, phase, value,
                 bias_or_weight=2, atk_request=None, rate=1):
        """
        :param name:    final_damage_buff
                        final_damage_debuff
        :param value:   倍数减 1，如 1.5倍填 0.5, 减伤填负数
        """
        super().__init__(timer, name, phase, value, bias_or_weight, atk_request, rate)


class ActPhaseBuff(Buff):
    """
    可行动阶段
    :param name:    act_phase
                    not_act_phase
                    no_normal_atk
    """
    pass


class PriorTargetBuff(Buff):
    """优先攻击目标"""
    def __init__(self, timer, name, phase, target: Target, ordered,
                 bias_or_weight=3, rate=1):
        """
        :param name:    prior_type_target
                        prior_loc_target
        :param ordered: bool
        """
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.target = target  # 筛选器，即 Target类
        self.ordered = ordered

    def activate(self, fleet, *args, **kwargs):
        prior = self.target.get_target(None, fleet)
        from src.wsgr.phase import AntiSubPhase, ShellingPhase, NightPhase
        if isinstance(self.timer.phase, (AntiSubPhase, ShellingPhase, NightPhase)):
            prior = [ship for ship in prior if ship.damaged < 4]
        if not len(prior):
            return None
        elif self.name == 'prior_loc_target':
            return prior[0]
        elif self.ordered:
            return prior[:1]
        else:
            return prior


class EventBuff(Buff):
    def is_event(self):
        return True

    def activate(self, atk, *args, **kwargs):
        pass


class ChaseAtkBuff(EventBuff):
    """追击技能"""
    def __init__(self, timer, phase,
                 name='chase', coef=None, exhaust=None,
                 atk_request=None, bias_or_weight=3, rate=1):
        super().__init__(timer, name, phase, bias_or_weight, rate)
        if coef is None:
            coef = {}
        self.coef = coef
        self.exhaust = exhaust
        self.atk_request = atk_request

    def is_active(self, atk, *args, **kwargs):
        if self.exhaust is not None and self.exhaust == 0:
            return False
        if not self.master.get_act_indicator():  # 无法行动时不能追击
            return False
        if atk.atk_body.side != self.master.side:  # 追击性质决定攻击者必须是友方
            return False
        from src.wsgr.formulas import SpecialAtk
        if not atk.target.can_be_atk(SpecialAtk):  # 只追击可以攻击的该敌方
            return False

        if self.atk_request is None:
            return isinstance(self.timer.phase, self.phase) and \
                   self.rate_verify()

        return isinstance(self.timer.phase, self.phase) and \
               bool(self.atk_request[0](self.timer, atk)) and \
               self.rate_verify()

    def activate(self, atk, *args, **kwargs):
        if self.exhaust is not None:
            self.exhaust -= 1

        from src.wsgr.formulas import SpecialAtk
        chase_atk = SpecialAtk(
            timer=self.timer,
            atk_body=self.master,
            def_list=None,
            coef=copy.copy(self.coef),
            target=atk.target
        )
        chase_atk.changable = False
        return chase_atk


class MagnetBuff(EventBuff):
    """嘲讽技能"""
    def __init__(self, timer, phase, rate,
                 name='magnet', atk_request=None, bias_or_weight=3):
        """
        :param rate:  嘲讽概率, 填入正数(30%填0.3)
        """
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.atk_request = atk_request

    def __repr__(self):
        return f"嘲讽: {self.rate * 100}%"

    def is_active(self, atk, *args, **kwargs):
        if not atk.changeable:
            return False
        if self.master.damaged == 4:
            return False

        if self.atk_request is None:
            return isinstance(self.timer.phase, self.phase) and \
                   self.master != atk.target and \
                   self.master in atk.def_list and \
                   self.rate_verify()

        return isinstance(self.timer.phase, self.phase) and \
               bool(self.atk_request[0](self.timer, atk)) and \
               self.master != atk.target and \
               self.master in atk.def_list and \
               self.rate_verify()

    def activate(self, atk, *args, **kwargs):
        atk.set_target(self.master)

    def change_rate(self, rate):
        # 嘲讽概率不会被让巴尔改变
        pass


class UnMagnetBuff(EventBuff):
    """负嘲讽技能"""
    def __init__(self, timer, phase, rate,
                 name='un_magnet', atk_request=None, bias_or_weight=3):
        """
        :param rate:  负嘲讽概率, 填入正数(30%填0.3)
        """
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.atk_request = atk_request

    def __repr__(self):
        return f"负嘲讽: {self.rate * 100}%"

    def is_active(self, atk, *args, **kwargs):
        if not atk.changeable:
            return False

        if self.atk_request is None:
            return isinstance(self.timer.phase, self.phase) and \
                   self.master == atk.target and \
                   self.rate_verify()

        return isinstance(self.timer.phase, self.phase) and \
               bool(self.atk_request[0](self.timer, atk)) and \
               self.master == atk.target and \
               self.rate_verify()

    def activate(self, atk, *args, **kwargs):
        target = np.random.choice(atk.def_list)
        atk.set_target(target)

    def change_rate(self, rate):
        # 负嘲讽概率不会被让巴尔改变
        pass


class TankBuff(EventBuff):
    """挡枪技能"""
    def __init__(self, timer, phase, target, value, rate,
                 name='tank', coef=None, exhaust=1, bias_or_weight=3):
        """
        :param target: 保护对象，class Target
        :param value: float, -1~0, 减伤率(负数)
        :param rate: float, 0~1, 发动率
        """
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.target = target
        self.exhaust = exhaust

        self.coef = {'must_hit': True,
                     'tank_damage_debuff': value}
        if coef is not None:
            self.coef.update(coef)

    def __repr__(self):
        return f"挡枪: {self.rate * 100}%"

    def is_active(self, atk, *args, **kwargs):
        if atk.target.side != self.master.side:  # 不为对面挡枪
            return False
        if self.exhaust is not None and self.exhaust == 0:
            return False
        if self.master.damaged >= 3:  # 大破状态不能发动
            return False

        self.change_value(atk, *args, **kwargs)
        def_target = self.target.get_target(atk.target.master, None)
        return isinstance(self.timer.phase, self.phase) and \
               self.master != atk.target and \
               atk.target in def_target and \
               self.rate_verify()

    def activate(self, atk, *args, **kwargs):
        atk.set_target(self.master)
        atk.set_coef(self.coef)
        if self.exhaust is not None:
            self.exhaust -= 1


class SpecialBuff(Buff):
    """机制增益"""
    def __init__(self, timer, name, phase,
                 exhaust=None, atk_request=None, bias_or_weight=3, rate=1):
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.exhaust = exhaust
        self.atk_request = atk_request

    def is_active(self, *args, **kwargs):
        if self.exhaust is not None and self.exhaust == 0:
            return False

        if self.atk_request is None:
            return isinstance(self.timer.phase, self.phase) and \
                   self.rate_verify()

        try:
            atk = kwargs['atk']
        except:
            atk = args[0]

        return isinstance(self.timer.phase, self.phase) and \
               bool(self.atk_request[0](self.timer, atk)) and \
               self.rate_verify()

    def activate(self, *args, **kwargs):
        if self.exhaust is not None:
            self.exhaust -= 1


class HitBack(SpecialBuff):
    def __init__(self, timer, phase,
                 name='hit_back', coef=None, exhaust=1,
                 atk_request=None, bias_or_weight=3, rate=1):
        super().__init__(timer, name, phase, exhaust, atk_request, bias_or_weight, rate)
        if coef is None:
            coef = {}
        self.coef = coef  # hit_back参数会在攻击结算时添加

    def is_active(self, atk, *args, **kwargs):
        if self.exhaust is not None and self.exhaust == 0:
            return False
        if atk.get_coef('hit_back'):  # 无法反击反击
            return False
        if not self.master.get_act_indicator():  # 无法行动时不能反击
            return False
        if self.master.damaged >= 3:  # 大破状态不能发动
            return False

        if self.atk_request is None:
            return isinstance(self.timer.phase, self.phase) and \
                   self.rate_verify()

        return isinstance(self.timer.phase, self.phase) and \
               bool(self.atk_request[0](self.timer, atk)) and \
               self.rate_verify()

    def activate(self, atk, *args, **kwargs):
        assert atk.atk_body.side != self.master.side  # 反击性质决定攻击者必须是敌方

        if self.exhaust is not None:
            self.exhaust -= 1

        from src.wsgr.phase import DaytimePhase
        if issubclass(self.phase, DaytimePhase):
            normal_atk = self.master.normal_atk
        else:
            normal_atk = self.master.night_atk

        hit_back = normal_atk(
            timer=self.timer,
            atk_body=self.master,
            def_list=None,
            coef=copy.copy(self.coef),
            target=atk.atk_body
        )
        hit_back.changable = False
        return hit_back


class ActiveBuff(Buff):
    """主动技能"""

    def __init__(self, timer, name, phase, num, rate,
                 during_buff: list = None, end_buff: list = None,
                 coef=None, bias_or_weight=3):
        """
        :param name:    multi_attack
                        extra_attack
                        special_attack
        :param num: 总攻击次数
        :param during_buff: 攻击期间buff
        :param end_buff: 攻击结束后buff
        """
        super().__init__(timer, name, phase, bias_or_weight, rate)
        if during_buff is None:
            during_buff = []
        self.during_buff = during_buff

        if end_buff is None:
            end_buff = []
        self.end_buff = end_buff

        self.num = num
        self.coef = coef

    def __repr__(self):
        return f'{self.name}: {self.rate}'

    def is_active_buff(self):
        return True

    def is_active(self, atk, enemy, *args, **kwargs):
        # if isinstance(enemy, list):
        #     def_list = enemy
        # elif isinstance(enemy, Fleet):
        #     def_list = enemy.get_atk_target(atk_type=atk)
        # else:
        #     raise TypeError('Enemy should be in form of list or Fleet')

        def_list = enemy.get_atk_target(atk_type=atk)
        return len(def_list) and \
               self.rate_verify() and \
               isinstance(self.timer.phase, self.phase)

    def active_start(self, atk, enemy, *args, **kwargs):
        """迭代器，依次执行攻击时效果、攻击行动、攻击后效果
        攻击结算时替换atk_list"""
        pass

    def add_during_buff(self):
        for tmp_buff in self.during_buff:
            self.master.temper_buff.append(tmp_buff)

    def remove_during_buff(self):
        for tmp_buff in self.during_buff:
            self.master.temper_buff.remove(tmp_buff)

    def add_end_buff(self):
        for tmp_buff in self.end_buff:
            self.master.add_buff(tmp_buff)


class MultipleAtkBuff(ActiveBuff):
    """多次攻击"""

    def active_start(self, atk, enemy, *args, **kwargs):
        assert self.master is not None
        def_list = enemy.get_atk_target(atk_type=atk)
        assert len(def_list)
        self.add_during_buff()  # 攻击时效果

        for i in range(self.num):
            if not len(def_list):
                break

            tmp_atk = atk(
                timer=self.timer,
                atk_body=self.master,
                def_list=def_list,
                coef=copy.copy(self.coef),
            )
            tmp_target = tmp_atk.target_init()
            def_list.remove(tmp_target)
            yield tmp_atk

        self.remove_during_buff()  # 去除攻击时效果
        self.add_end_buff()  # 攻击结束效果


class ExtraAtkBuff(ActiveBuff):
    """连续攻击"""

    def active_start(self, atk, enemy, *args, **kwargs):
        assert self.master is not None
        def_list = enemy.get_atk_target(atk_type=atk)
        assert len(def_list)
        self.add_during_buff()  # 攻击时效果

        atk_sample = atk(
            timer=self.timer,
            atk_body=self.master,
            def_list=def_list,
            coef=copy.copy(self.coef),
        )
        tmp_target = atk_sample.target_init()
        yield atk_sample

        for i in range(self.num - 1):
            if tmp_target.damaged == 4:
                break
            tmp_atk = atk(
                timer=self.timer,
                atk_body=self.master,
                def_list=def_list,
                coef=copy.copy(self.coef),
                target=tmp_target,
            )
            yield tmp_atk

        self.remove_during_buff()  # 去除攻击时效果
        self.add_end_buff()  # 攻击结束效果


class SpecialAtkBuff(ActiveBuff):
    """特殊攻击(在一次攻击内执行多个不同效果，可能同时包含攻击前攻击后)"""

    def __init__(self, timer, phase, rate,
                 name='special_attack', num=1,
                 during_buff: list = None, end_buff: list = None,
                 target: Target = None, atk_type=None,
                 undamaged=False,
                 coef=None, bias_or_weight=3):
        super().__init__(timer, name, phase, num, rate,
                         during_buff, end_buff, coef, bias_or_weight)
        self.target = target
        self.atk_type = atk_type
        self.undamaged = undamaged  # True: 大破状态不能发动, False: 大破状态可以发动

    def get_def_list(self, atk_type, enemy):
        # 获取可被攻击的对象
        def_list = enemy.get_atk_target(atk_type=atk_type)

        # 如果指定了攻击目标，筛选出对应敌舰
        if self.target is not None:
            def_list = self.target.get_target(None, def_list)

        return def_list

    def is_active(self, atk, enemy, *args, **kwargs):
        # 如果技能指定了攻击类型，使用对应攻击类型
        if self.atk_type is not None:
            atk_type = self.atk_type
        else:
            atk_type = atk
        if self.undamaged and self.master.damaged >= 3:  # 大破状态不能发动
            return False

        def_list = self.get_def_list(atk_type, enemy)  # 可被攻击目标

        return len(def_list) and \
               self.rate_verify() and \
               isinstance(self.timer.phase, self.phase)

    def active_start(self, atk, enemy, *args, **kwargs):
        assert self.master is not None

        # 如果技能指定了攻击类型，使用对应攻击类型
        if self.atk_type is not None:
            atk_type = self.atk_type
        else:
            atk_type = atk

        self.add_during_buff()  # 攻击时效果
        def_list = self.get_def_list(atk_type, enemy)  # 可被攻击目标

        # 技能优先攻击特定船型
        prior = self.master.get_prior_type_target(enemy)
        if prior is not None:
            def_list = prior

        if len(def_list) > 0:
            spetial_atk = atk_type(
                timer=self.timer,
                atk_body=self.master,
                def_list=def_list,
                coef=copy.copy(self.coef),
            )
            yield spetial_atk

        self.remove_during_buff()  # 去除攻击时效果
        self.add_end_buff()  # 攻击结束效果
