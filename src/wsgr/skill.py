# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 技能类

import numpy as np
import copy

from src.wsgr.wsgrTimer import Time
from src.wsgr.ship import Ship, Fleet
from src.wsgr.phase import *


class Skill(Time):
    def __init__(self, timer, master):
        super().__init__(timer)
        self.master = master

        self.request = None  # list of Request, not initialised
        self.target = None  # Target
        self.buff = None  # list of Buff

    def is_active(self, friend, enemy):
        """技能是否满足发动条件, 默认True, 子类根据需要重新定义"""
        # bool(request(self.master, friend, enemy))
        return True

    def activate(self, friend, enemy):
        """技能生效时, 给所有满足条件的目标套上所有buff"""
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                tmp_target.add_buff(tmp_buff)

    def is_common(self):
        return False


class CommonSkill(Skill):
    """仅包含常驻面板加成的技能"""
    def is_common(self):
        return True


class EquipSkill(Skill):
    """装备携带特效"""

    def __init__(self, timer, master, value: list):
        super().__init__(timer, master)
        self.value = value

    def activate(self, friend, enemy):
        """技能生效时, 给所有满足条件的目标套上所有buff"""
        target = self.target.get_target(friend, enemy)
        for tmp_target in target:
            for tmp_buff in self.buff[:]:
                buff_type = tmp_buff.effect_type

                # 2类不叠加
                if buff_type in [2.1, 2.2]:
                    type2 = tmp_target.get_unique_effect(effect_type=buff_type)

                    # 有2类特效，跳过
                    if type2 is not None:
                        continue

                # 3和4类不叠加
                elif buff_type in [3, 4]:
                    type34 = tmp_target.get_unique_effect(effect_type=[3, 4])

                    # 无3和4类特效
                    if type34 is None:
                        pass

                    # 特效类型不同，跳过
                    elif type34.effect_type != buff_type:
                        continue

                    # 特效类型相同，取最高值
                    else:
                        value1 = tmp_buff.value
                        value2 = type34.value
                        type34.set_value(max(value1, value2))
                        continue

                tmp_target.add_buff(tmp_buff)


class Request(Time):
    """技能发动条件"""

    def __init__(self, timer, master, friend, enemy):
        super().__init__(timer)
        self.master = master
        self.friend = friend
        self.enemy = enemy

    def __bool__(self):
        pass


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


class SelfTarget(Target):
    """自身buff"""
    def __init__(self, master, side=1):
        super().__init__(side)
        self.master = master

    def get_target(self, friend, enemy):
        return [self.master]


class TypeTarget(Target):
    """指定船型的目标"""
    def __init__(self, side, shiptype):
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


class RandomTypeTarget(TypeTarget):
    """指定船型内随机选择一个目标"""
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
        target = np.random.choice(target)
        return [target]


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


class LocTarget(Target):
    """指定站位的目标"""
    def __init__(self, side, loc: list):
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
        距离最近的(上方/下方/相邻)，可指定船型
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
        count = self.radius
        index = fleet.index(self.master)  # 技能所有者在list内的索引
        loc = self.master.loc  # 技能所有者的实际站位
        gap = loc - index  # 实际列表索引与编队索引的差距
        while count > 0 and index > 0:
            index -= 1  # 向前推进一位
            tmp_ship = fleet[index]

            # 站位检测，不等说明中间跳过了单位
            if tmp_ship.loc != index + gap:
                gap -= 1
                index += 1

            # 满足条件时加入返回列表，同时计数-1
            elif isinstance(tmp_ship, self.shiptype):
                target.append(tmp_ship)
                count -= 1
                continue

            # 不满足条件时，判断能否顺延，不能顺延时计数-1
            if not self.expand:
                count -= 1

        return target

    def get_down_target(self, fleet):
        if isinstance(fleet, Fleet):
            fleet = fleet.ship

        target = []
        count = self.radius
        index = fleet.index(self.master)  # 技能所有者在list内的索引
        loc = self.master.loc  # 技能所有者的实际站位
        gap = loc - index  # 实际列表索引与编队索引的差距
        while count > 0 and index < len(fleet):
            index += 1  # 向后推进一位
            tmp_ship = fleet[index]

            # 站位检测，不等说明中间跳过了单位
            if tmp_ship.loc != index + gap:
                gap += 1
                index -= 1

            # 满足条件时加入返回列表，同时计数-1
            elif isinstance(tmp_ship, self.shiptype):
                target.append(tmp_ship)
                count -= 1
                continue

            # 不满足条件时，判断能否顺延，不能顺延时计数-1
            if not self.expand:
                count -= 1

        return target


class TagTarget(Target):
    """指定标签的目标"""

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


class StatusTarget(Target):
    """指定属性的目标"""

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
                      if ship.get_status(self.status_name) == self.value]
        elif self.fun == 'ge':
            target = [ship for ship in fleet
                      if ship.get_status(self.status_name) >= self.value]
        elif self.fun == 'gt':
            target = [ship for ship in fleet
                      if ship.get_status(self.status_name) > self.value]
        elif self.fun == 'le':
            target = [ship for ship in fleet
                      if ship.get_status(self.status_name) <= self.value]
        elif self.fun == 'lt':
            target = [ship for ship in fleet
                      if ship.get_status(self.status_name) < self.value]
        else:
            raise ValueError()
        return target


class EquipTarget(Target):
    """装备"""
    def __init__(self, side, target, equiptype):
        super().__init__(side)
        self.target = target  # Target, 描述目标装备的携带者
        self.equiptype = equiptype  # tuple, 目标装备类型

    def get_target(self, friend, enemy):
        """返回目标对象所携带的满足条件的装备对象"""
        ship_target = self.target.get_target(friend, enemy)
        equip_target = []
        for tmp_ship in ship_target:
            for tmp_equip in tmp_ship.equipment:
                if isinstance(tmp_equip, self.equiptype):
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

    def is_common(self):
        return False

    def is_event(self):
        return False

    def is_active_buff(self):
        return False

    def is_equip_effect(self):
        return False

    def is_coef_process(self):
        return False

    def is_switch(self):
        return False

    def is_active(self, *args, **kwargs):
        """技能是否满足发动阶段"""
        return self.rate_verify() and \
               isinstance(self.timer.phase, self.phase)

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


class CoeffBuff(Buff):
    """系数增益"""
    def __init__(self, timer, name, phase, value, bias_or_weight, rate=1):
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.value = value

    def __repr__(self):
        return f"{self.name}: {self.value}"


class EquipEffect(Buff):
    """装备自带特效"""

    def __init__(self, timer, effect_type, name, phase, value, bias_or_weight, rate=1):
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.value = value
        self.effect_type = effect_type

    def __repr__(self):
        return f"{self.name}: {self.value}(装备特效{self.effect_type})"

    def is_equip_effect(self):
        return True

    def set_value(self, value):
        self.value = value


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


class AtkHitBuff(Buff):
    """命中后效果"""
    def __init__(self, timer, name, phase, buff, side,
                 atk_request=None, bias_or_weight=3, rate=1):
        """
        :param buff: 施加效果内容
        :param side: 给谁加, 0: 被攻击者; 1: 攻击者
        :param atk_request: ATKRequest, 攻击判断(攻击者、被攻击者、攻击类型)
        """
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.buff = buff
        self.side = side
        self.atk_request = atk_request

    def is_active(self, *args, **kwargs):
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
        try:
            atk = kwargs['atk']
        except:
            atk = args[0]

        if (self.name == 'atk_hit' and self.side == 1) or \
                (self.name == 'be_atk_hit' and self.side == 0):
            target = atk.atk_body
        else:
            target = atk.target

        for tmp_buff in self.buff[:]:
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
        super().__init__(timer, name, phase, value, bias_or_weight, atk_request, rate)


class SpecialBuff(Buff):
    """机制增益"""
    def __init__(self, timer, name, phase,
                 exhaust=None, atk_request=None, bias_or_weight=3, rate=1):
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.exhaust = exhaust
        self.atk_request = atk_request

    def is_active(self, *args, **kwargs):
        if self.exhaust is None:
            exhaust_flag = True
        elif self.exhaust > 0:
            exhaust_flag = True
        else:
            exhaust_flag = False

        if self.atk_request is None:
            return isinstance(self.timer.phase, self.phase) and \
                   self.rate_verify() and exhaust_flag

        try:
            atk = kwargs['atk']
        except:
            atk = args[0]

        return isinstance(self.timer.phase, self.phase) and \
               bool(self.atk_request[0](self.timer, atk)) and \
               self.rate_verify() and exhaust_flag

    def activate(self, *args, **kwargs):
        if self.exhaust is not None:
            self.exhaust -= 1


class ActPhaseBuff(Buff):
    """可行动阶段"""
    pass


class PriorTargetBuff(Buff):
    """优先攻击目标"""
    def __init__(self, timer, name, phase, target, ordered):
        super().__init__(timer, name, phase)
        self.target = target
        self.ordered = ordered

    def activate(self, fleet, *args, **kwargs):
        prior = self.target.get_target(None, fleet)
        if not len(prior):
            return None
        elif self.ordered:
            return prior[0]
        else:
            return np.random.choice(prior)


class EventBuff(Buff):
    def is_event(self):
        return True


class MagnetBuff(EventBuff):
    """嘲讽技能"""
    def __init__(self, timer, phase, rate,
                 name='magnet', atk_request=None, bias_or_weight=3):
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.atk_request = atk_request

    def __repr__(self):
        return f"嘲讽: {self.rate}"

    def is_active(self, atk, *args, **kwargs):
        if not atk.changeable:
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


class UnMagnetBuff(EventBuff):
    """负嘲讽技能"""
    def __init__(self, timer, phase, master, rate,
                 name='un_magnet', atk_request=None, bias_or_weight=3):
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.master = master
        self.atk_request = atk_request

    def __repr__(self):
        return f"负嘲讽: {self.rate}"

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


class TankBuff(EventBuff):
    """挡枪技能"""
    pass


class ActiveBuff(Buff):
    """主动技能"""

    def __init__(self, timer, phase, num, target, buff, rate,
                 coef=None, name='multiple_attack', bias_or_weight=3):
        super().__init__(timer, name, phase, bias_or_weight, rate)
        self.target = target
        self.buff = buff
        self.num = num
        self.coef = coef

    def is_active_buff(self):
        return True

    def activate(self, atk, enemy, *args, **kwargs):
        atk_list = []
        return atk_list


class MultipleAtkBuff(ActiveBuff):
    """多次攻击"""

    def activate(self, atk, enemy, *args, **kwargs):
        assert self.master is not None
        def_list = enemy.get_atk_target(atk_type=atk)
        atk_list = []
        for i in range(self.num):
            if not len(def_list):
                break

            tmp_atk = atk(
                timer=self.timer,
                atk_body=self.master,
                def_list=def_list,
                coef=self.coef,
            )
            tmp_atk.target_init()
            def_list.remove(tmp_atk.target)
            atk_list.append(tmp_atk)

        return atk_list


class ExtraAtkBuff(ActiveBuff):
    """连续攻击"""

    def activate(self, atk, enemy, *args, **kwargs):
        assert self.master is not None
        def_list = enemy.get_atk_target(atk_type=atk)
        atk_list = []
        if not len(def_list):
            return atk_list

        atk_sample = atk(
            timer=self.timer,
            atk_body=self.master,
            def_list=def_list,
            coef=self.coef,
        )
        atk_sample.target_init()

        for i in range(self.num):
            tmp_atk = copy.deepcopy(atk_sample)
            atk_list.append(tmp_atk)

        del atk_sample
        return atk_list


# class SwitchBuff(AtkBuff):
#     """攻击期间、攻击后生效buff"""
#     def __init__(self, timer, name, phase, value, switch, bias_or_weight,
#                  atk_request=None, rate=1):
#         super().__init__(timer, name, phase, value, bias_or_weight, atk_request, rate)
#         self.switch = switch
#
#     def is_switch(self):
#         return True
#
#     def switch_on(self):
#         self.switch = True
#
#     def switch_off(self):
#         self.switch = False
#
#     def is_active(self, *args, **kwargs):
#         if self.atk_request is None:
#             return self.switch and \
#                    isinstance(self.timer.phase, self.phase) and \
#                    self.rate_verify()
#
#         try:
#             atk = kwargs['atk']
#         except:
#             atk = args[0]
#
#         return self.switch and \
#                isinstance(self.timer.phase, self.phase) and \
#                bool(self.atk_request[0](self.timer, atk)) and \
#                self.rate_verify()
