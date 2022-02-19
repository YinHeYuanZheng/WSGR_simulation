# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 技能类

from .wsgrTimer import Time
from .ship import Fleet


class Skill(Time):
    def __init__(self, master):
        super().__init__()
        self.master = master

        self.request = None  # list of Request, not initialised
        self.target = None  # Target
        self.buff = None  # list of Buff

    def is_active(self, friend, enemy):
        """技能是否满足发动条件, 默认True, 子类需要重新定义"""
        # bool(request(self.master, friend, enemy))
        return True

    def activate(self, friend, enemy):
        """技能生效时, 给所有满足条件的目标套上所有buff"""
        target = self.target.get_target(friend, enemy)
        for tmp_ship in target:
            for tmp_buff in self.buff:
                tmp_ship.add_buff(tmp_buff)

    def is_common(self):
        return False


class CommonSkill(Skill):
    """仅包含常驻面板加成的技能"""
    def is_common(self):
        return True


class Request(Time):
    """技能发动条件"""

    def __init__(self, master, friend, enemy):
        super().__init__()
        self.master = master
        self.friend = friend
        self.enemy = enemy

    def __bool__(self):
        pass


class ATKRequest(Request):
    """判断攻击类型、攻击目标等，备用"""
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
    def __init__(self, side, shiptype: tuple):
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


class LocTarget(Target):
    """指定站位的目标"""
    def __init__(self, side, loc):
        super().__init__(side)
        self.loc = loc


class TagTarget(Target):
    """指定标签的目标"""
    pass


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
                      if ship.status[self.status_name] == self.value]
        elif self.fun == 'ge':
            target = [ship for ship in fleet
                      if ship.status[self.status_name] >= self.value]
        elif self.fun == 'gt':
            target = [ship for ship in fleet
                      if ship.status[self.status_name] > self.value]
        elif self.fun == 'le':
            target = [ship for ship in fleet
                      if ship.status[self.status_name] <= self.value]
        elif self.fun == 'lt':
            target = [ship for ship in fleet
                      if ship.status[self.status_name] < self.value]
        else:
            raise ValueError()
        return target


class EquipTarget(Target):
    """装备"""
    def __init__(self, side, target: Target, equiptype: tuple):
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
    def __init__(self, name, phase: tuple, bias_or_weight=3):
        super().__init__()
        self.master = None
        self.name = name  # 检索用名称
        self.phase = phase  # 发动阶段, tuple

        # flag, 0: bias; 1: weight add; 2: weight mult; 3: not available
        self.bias_or_weight = bias_or_weight

    def set_master(self, master):
        self.master = master

    def is_common(self):
        return False

    def is_event(self):
        return False

    def in_phase(self):
        """技能是否满足发动阶段"""
        return isinstance(self.timer.phase, self.phase)


class StatusBuff(Buff):
    """属性增益"""
    def __init__(self, name, phase, value, bias_or_weight):
        super().__init__(name, phase, bias_or_weight)
        self.value = value


class CommonBuff(StatusBuff):
    """常驻增益(通常直接显示在面板上)"""
    def is_common(self):
        return True


class CoeffBuff(Buff):
    """系数增益"""
    def __init__(self, name, phase, value, bias_or_weight):
        super().__init__(name, phase, bias_or_weight)
        self.value = value


class SpecialBuff(Buff):
    """机制增益"""
    pass


class AtkCoefProcess(SpecialBuff):
    """直接修改攻击属性(船损、航向、制空系数等)"""
    pass


class FinalDamageBuff(Buff):
    """终伤系数, 乘算, 需要判断攻击类型"""
    def __init__(self, name, phase, value, atk_request: tuple, bias_or_weight=2):
        super().__init__(name, phase, bias_or_weight)
        self.value = value
        self.atk_request = atk_request

    def is_atk_type(self, atk):
        # todo 更改成ATKRequest
        return isinstance(atk, self.atk_request)


class EventBuff(Buff):
    def is_event(self):
        return True
