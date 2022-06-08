# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

from src.wsgr.wsgrTimer import Time
from src.utils import battleUtil
import src.wsgr.ship as rship
import src.wsgr.equipment as requip
from src import skillCode


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
            p = Point(name)

            # 写入节点属性
            battle_type = status.pop('type')
            p.set_type(getattr(battleUtil, battle_type))
            p_level = status.pop('level')
            p.set_level(p_level)
            roundabout = status.pop('roundabout')
            p.set_roundabout(roundabout)

            # 生成深海舰队
            enemy_list = []
            enemy_status = status.pop('enemy')
            for enemy_ids in enemy_status:
                if enemy_ids[0] != '':
                    fleet = self.load_fleet(enemy_ids, dataset, self.timer)
                    enemy_list.append(fleet)
            p.set_enemy(enemy_list)

            # 生成后继节点及带路
            suc = self.load_suc(n)
            p.set_suc(suc)

            if name in ['a', 'b']:
                self.point['entrance'] = p
            else:
                self.point[name] = p

    def load_fleet(self, enemy_ids, dataset, timer):
        fleet = rship.Fleet(timer)
        fleet.set_form(int(enemy_ids[0]))

        shiplist = []
        for i in range(len(enemy_ids) - 1):
            cid = enemy_ids[i + 1]
            if cid != '':
                ship = self.load_ship(cid, len(shiplist) + 1, dataset, timer)
                ship.set_master(fleet)
                shiplist.append(ship)

        assert len(shiplist) != 0
        fleet.set_ship(shiplist)
        fleet.set_side(0)
        return fleet

    def load_ship(self, cid, loc, dataset, timer):
        # 读取舰船属性
        status = dataset.get_enemy_ship_status(cid)

        # 舰船对象实例化
        ship_type = status.pop('type')
        ship = getattr(rship, ship_type)(timer)  # 根据船型获取类，并实例化
        ship.set_cid(cid)

        # 写入固有属性
        ship.set_loc(int(loc))
        ship.set_level(50)
        ship.set_affection(50)

        if status['capacity'] != 0:
            load = status.pop('load')
            ship.set_load(load)
        eid_list = status.pop('equip')
        skill_list = status.pop('skill')

        # 写入舰船属性
        ship.set_status(status=status)
        del status

        # 调用技能并写入
        skill_num = 0  # 默认只有一个技能
        sid = skill_list[skill_num]
        if sid != '':
            sid = 'sid' + sid
            skill = getattr(skillCode, sid).skill  # 根据技能设置获取技能列表，未实例化
            ship.add_skill(skill)
            del skill

        # 读取装备属性并写入
        for i, eid in enumerate(eid_list):
            if eid != '':
                estatus = dataset.get_equip_status(eid)
                equip_type = estatus.pop('type')
                equip = getattr(requip, equip_type)(timer, ship, i + 1)  # 根据装备类型获取类，并实例化

                # 如果装备也存在特殊效果，当作技能写入舰船skill内
                esid = estatus.pop('skill')
                if esid != '':
                    esid = 'esid' + esid
                    skill = getattr(skillCode, esid).skill  # 根据技能设置获取技能列表，未实例化
                    equip.add_skill(skill)  # 写入装备技能

                # 写入装备属性
                equip.set_status(status=estatus)
                ship.set_equipment(equip)

        return ship

    def load_suc(self, node):
        suc_list = node.getElementsByTagName('point')
        suc = {}
        for suc_node in suc_list:
            name = suc_node.getAttribute('name')
            weight = suc_node.getAttribute('weight')
            suc[name] = Successor(weight, suc_node)
        return suc

    def start(self):
        pass


class Point:
    """节点基类"""

    def __init__(self, name):
        self.name = name
        self.type = None
        self.level = 0
        self.roundabout = None
        self.enemy_list = []
        self.suc = {}

    def __repr__(self):
        return f'{self.name}({self.level})'

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

    def set_roundabout(self, roundabout):
        """
        能否迂回
        :param roundabout: bool
        """
        self.roundabout = roundabout

    def set_enemy(self, enemy_list):
        self.enemy_list = enemy_list

    def set_suc(self, suc_dic):
        self.suc = suc_dic


class Successor:
    def __init__(self, weight, request):
        self.weight = weight
        self.request = request

    def bool(self, friend_fleet):
        if not len(self.request):
            return False

        flag = True
        for tmp_request in self.request:
            flag = flag and tmp_request.bool(friend_fleet)
        return flag


class LeadRequest:
    def __init__(self):
        pass
