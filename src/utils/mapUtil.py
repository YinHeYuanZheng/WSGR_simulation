# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

from src.wsgr.wsgrTimer import Time
from src.utils import battleUtil


class MapUtil(Time):
    """地图调用基类"""

    def __init__(self, timer, entrance, dataset, friend):
        super().__init__(timer)
        self.friend = friend
        self.point = {}
        self.init_map(entrance, dataset)

    def init_map(self, entrance, dataset):
        """根据xml结构和数据库，构建海图"""
        points = entrance.getElementsByTagName('point')
        for n in points:
            # 读取节点属性
            name = n.getAttribute('name')
            pid = n.getAttribute('pid')
            status = dataset.get_point_status(pid)
            p = Point()

            battle_type = status.pop('type')
            p.set_type(getattr(battleUtil, battle_type))
            p_level = status.pop('level')
            p.set_level(p_level)

            if name in ['a', 'b']:
                self.point['entrance'] = p
            else:
                self.point[name] = p

    def start(self):
        pass


class Point:
    """节点基类"""

    def __init__(self):
        self.type = None
        self.level = None

    def set_type(self, battle_type):
        """
        :param battle_type: class battleUtil.BattleUtil
        """
        self.type = battle_type

    def set_level(self, level):
        """
        节点等级
        :param level: 0: 起点, 1: 出门, 2: 道中, 3: 门神, 4: 非boss地图终点, 5: boss
        """
        self.level = level
