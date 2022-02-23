# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38
# 装备类

import numpy as np
# import sys
# sys.path.append(r'.\wsgr')

from .wsgrTimer import Time


class Equipment(Time):
    """装备总类"""

    def __init__(self, master, enum):
        super().__init__()
        self.master = master  # 该装备载体
        self.enum = enum  # 该装备所在栏位
        self.status = {}  # 装备属性
        self.common_buff = []  # 永久面板加成(如驻岛舰队、巨像、汉考克)
        self.temper_buff = []  # 临时buff

    def get_status(self, name):
        """根据属性名称获取装备属性，包含常驻面板加成"""
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


class Plane(Equipment):
    """飞机"""
    def __init__(self, master, enum):
        super().__init__(master, enum)
        self.load = self.master.load[self.enum]

    def fall(self, fall_num):
        buff_scale, buff_bias = self.master.get_buff('fall_rest')
        fall_num = np.ceil(fall_num * (1 + buff_scale) + buff_bias)
        self.load -= int(fall_num)


class Bomber(Plane):
    pass


class DiveBomber(Plane):
    pass


class Fighter(Plane):
    """战斗机"""
    def fall(self, fall_num):
        if self.load < fall_num:
            fall_num = self.load
        self.load -= int(fall_num)


class ScoutPLane(Plane):
    pass


class MainGun(Equipment):
    """主炮"""
    pass


class SecondaryGun(Equipment):
    """副炮"""
    pass


class AntiAirGun(Equipment):
    """防空炮"""
    def __init__(self, master, enum):
        super().__init__(master, enum)
        # self.status['aa_scale'] = 1.  # 防空倍率
        # self.status['aa_coef'] = 0.  # 补正倍率
