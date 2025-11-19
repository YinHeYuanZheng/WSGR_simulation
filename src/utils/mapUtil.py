# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import numpy as np

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
        for node in points:
            # 读取节点属性
            name = node.getAttribute('name')
            pid = node.getAttribute('pid')
            status = dataset.get_point_status(pid)
            level = int(node.getAttribute('level'))
            p = Point(name, level)

            # 写入节点属性
            battle_type = status.pop('type')
            p.set_type(getattr(battleUtil, battle_type))
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
            suc = self.load_suc(node)  # 带路包含在节点属性内
            if (p.level in [0, 1, 2, 3]) and (len(suc) == 0):
                raise ValueError(f'Point {name} should have successor(s)!')
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
        # ship.set_level(50)
        ship.set_affection(50)

        # 写入非属性变量
        level = status.pop('level')
        ship.set_level(level)
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

            # 获取技能名称并输出
            try:
                skill_name = getattr(skillCode, sid).name
                print(f"{ship.status['name']} {skill_name}")
            except:
                print(f"{ship.status['name']} 未获取到技能名称")

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
        suc_list = node.getElementsByTagName('suc')
        suc = {}
        for suc_node in suc_list:
            name = suc_node.getAttribute('name')
            weight = float(suc_node.getAttribute('weight'))
            relation = suc_node.getAttribute('relation')
            request = self.load_request(suc_node)
            suc[name] = Successor(weight, request, relation)
        return suc

    def load_request(self, node):
        req_list = node.getElementsByTagName('request')
        request = []
        for req_node in req_list:
            request.append(
                LeadRequest(
                    request_type=req_node.getAttribute('type'),
                    name=req_node.getAttribute('name'),
                    fun=req_node.getAttribute('fun'),
                    value=req_node.getAttribute('value'),
                )
            )
        return request

    def start(self):
        name = 'entrance'
        while name is not None:
            point = self.point[name]
            name = point.start(self.timer, self.friend)

    def report(self):
        # 消耗
        supply = self.timer.log['supply']
        for tmp_ship in self.friend.ship:
            ship_supply = tmp_ship.reset()
            supply['oil'] += int(ship_supply['oil'])
            supply['ammo'] += int(ship_supply['ammo'])
            supply['steel'] += int(ship_supply['steel'])
            supply['almn'] += int(ship_supply['almn'])
        self.timer.report_log('supply', supply)

        return self.timer.log


class Point:
    """节点基类"""

    def __init__(self, name, level):
        self.name = name
        self.level = level  # 节点等级, 0: 起点, 1: 出门, 2: 道中, 3: 门神, 4: 非boss地图终点, 5: boss
        self.type = None
        self.roundabout = None
        self.enemy_list = []
        self.suc = {}

        self.battle = None

    def __repr__(self):
        return f'{self.name}({self.level})'

    def set_type(self, battle_type):
        """
        :param battle_type: class battleUtil.BattleUtil
        """
        self.type = battle_type

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

    def start(self, timer, friend):
        """创建战斗类并移动到下个点"""
        timer.set_point(self)

        # todo 阵型策略（道中复纵 boss梯形）
        if self.level != 5:
            friend.set_form(2)
        else:
            friend.set_form(4)

        if len(self.enemy_list) != 0:
            enemy = np.random.choice(self.enemy_list)
            self.battle = self.type(timer, friend, enemy)
        else:
            self.battle = self.type(timer, friend, None)
        self.battle.start()
        return self.move(friend)

    def move(self, friend):
        self.battle.timer.log['end_with'] = self.name
        # 地图终点
        if not len(self.suc):
            assert self.level in [4, 5]
            if self.level == 5:
                self.battle.timer.log['end_with_boss'] = True
            return None

        # todo 迂回失败回港
        # if self.roundabout and \
        #         not self.battle.timer.round_flag:
        #     return None

        for tmp_ship in friend.ship:
            # 大破不再前进
            if tmp_ship.damaged >= 3:
                return None

            # 油弹耗尽不再前进
            if tmp_ship.supply_oil <= 0 or tmp_ship.supply_ammo <= 0:
                return None

        # 带路检定
        for name, suc_point in self.suc.items():
            if suc_point.bool(friend):
                return name

        # 随机沟
        weight = np.array([suc.weight for suc in self.suc.values()])
        normalized_weight = weight / np.sum(weight)
        next_name = np.random.choice(list(self.suc.keys()), p=normalized_weight)
        return next_name


class Successor:
    def __init__(self, weight, request, relation):
        self.weight = weight
        self.request = request
        self.relation = relation

    def bool(self, friend_fleet):
        if len(self.request) == 0:
            return False

        elif len(self.request) == 1:
            return self.request[0].bool(friend_fleet)

        elif self.relation == 'or':
            for tmp_request in self.request:
                if tmp_request.bool(friend_fleet):
                    return True
            return False

        else:
            for tmp_request in self.request:
                if not tmp_request.bool(friend_fleet):
                    return False
            return True


class LeadRequest:
    def __init__(self, request_type, name, fun, value):
        self.request_type = request_type
        self.name = name
        self.fun_name = fun
        if value == '':
            self.value = value
        else:
            self.value = float(value)

        self._request = None
        self._fun = None

        self.gen_request()
        self.gen_fun()

    def gen_request(self):
        if self.request_type == 'num':
            name = self.name.split(',')
            shiptype = tuple([getattr(rship, type_name) for type_name in name])
            self._request = lambda x: \
                len([ship for ship in x.ship if isinstance(ship, shiptype)])

        elif self.request_type == 'leader':
            name = self.name.split(',')
            shiptype = tuple([getattr(rship, type_name) for type_name in name])
            self._request = lambda x: isinstance(x.ship[0], shiptype)

        elif self.request_type == 'status':
            self._request = lambda x: x.status[self.name]

        else:
            raise ValueError(f'Wrong request type {self.request_type}')

    def gen_fun(self):
        if self.fun_name == 'lt':
            self._fun = lambda x, y: x < y

        elif self.fun_name == 'le':
            self._fun = lambda x, y: x <= y

        elif self.fun_name == 'eq':
            self._fun = lambda x, y: x == y

        elif self.fun_name == 'ge':
            self._fun = lambda x, y: x >= y

        elif self.fun_name == 'gt':
            self._fun = lambda x, y: x > y

        elif self.fun_name == 'is':
            self._fun = lambda x, y: x

        elif self.fun_name == 'not':
            self._fun = lambda x, y: not x

        else:
            raise ValueError()

    def bool(self, friend_fleet):
        return self._fun(self._request(friend_fleet), self.value)
