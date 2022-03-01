# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 装备类

import numpy as np
from src.wsgr.wsgrTimer import Time
from src.wsgr.ship import *


class Equipment(Time):
    """装备总类"""

    def __init__(self, timer, master, enum):
        super().__init__(timer)
        self.master = master  # 该装备载体
        self.enum = enum  # 该装备所在栏位
        self.status = {}  # 装备属性
        self.common_buff = []  # 永久面板加成(如驻岛舰队、巨像、汉考克)
        self.temper_buff = []  # 临时buff

    def __repr__(self):
        return f"{type(self).__name__}: {self.status['name']}"

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
        """根据属性名称获取装备属性，包含常驻面板加成"""
        status = self.status.get(name, 0)

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

    def get_final_status(self, name):
        """根据属性名称获取最终属性"""
        buff_scale, buff_bias = self.get_buff(name)
        status = self.get_status(name) * (1 + buff_scale) + buff_bias
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
        """根据增益名称获取全部攻击系数增益(含攻击判断)(目前只有命中调用)"""
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


class Plane(Equipment):
    """飞机"""
    def __init__(self, timer, master, enum):
        super().__init__(timer, master, enum)
        self.load = self.master.load[self.enum - 1]

    def __repr__(self):
        return f"{type(self).__name__}: {self.status['name']} " \
               f"({self.load}/{self.master.load[self.enum-1]})"

    def fall(self, fall_num):
        fall_num = min(self.load, fall_num)
        self.load -= int(fall_num)


class Bomber(Plane):
    pass


class DiveBomber(Plane):
    pass


class Fighter(Plane):
    """战斗机"""
    pass


class ScoutPLane(Equipment):
    pass


class MainGun(Equipment):
    """主炮"""
    pass


class SecondaryGun(Equipment):
    """副炮"""
    pass


class AntiAirGun(Equipment):
    """防空炮"""
    pass


class Radar(Equipment):
    pass


class Torpedo(Equipment):
    """鱼雷"""
    pass


class DepthMine(Equipment):
    """深投"""
    pass


class Sonar(Equipment):
    pass


class Shell(Equipment):
    """炮弹"""
    pass


class Accessory(Equipment):
    """强化部件"""
    pass
