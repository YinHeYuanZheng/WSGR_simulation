# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import xml.dom.minidom

from .. import battleUtil
from ..wsgr.ship import *
from ..wsgr import ship as rship
from .. import skillCode


def load_config(config, dataset):
    """加载配置文件"""
    dom = xml.dom.minidom.parse(config)
    root = dom.documentElement

    friend_root = root.getElementsByTagName('Fleet')[0]
    friend = load_fleet(friend_root, dataset)

    enemy_root = root.getElementsByTagName('Fleet')[1]
    enemy = load_fleet(enemy_root, dataset)

    # 根据战斗类型调用不同流程类
    battle_type = root.getAttribute('type')
    battle = getattr(battleUtil, battle_type)

    return battle(friend, enemy)


def load_fleet(node, dataset):
    fleet = Fleet()
    fleet.set_form(int(node.getAttribute('form')))

    shiplist = []
    for i in range(len(node.getElementsByTagName('Ship'))):
        s_node = node.getElementsByTagName('Ship')[i]
        ship = load_ship(s_node, dataset)
        shiplist.append(ship)

    fleet.set_ship(shiplist)
    fleet.set_side(int(node.getAttribute('side')))
    return fleet


def load_ship(node, dataset):
    # 舰船对象实例化
    cid = node.getAttribute('cid')
    ship_type = node.getAttribute('type')
    ship = getattr(rship, ship_type)()  # 根据船型获取类，并实例化
    ship.set_cid(cid)

    # 写入节点属性
    ship.set_loc(node.getAttribute('loc'))
    ship.set_level(node.getAttribute('level'))
    ship.set_affection(node.getAttribute('affection'))

    # 读取舰船属性并写入
    status = dataset.get_ship_status(cid)
    if isinstance(ship, Aircraft):
        assert status['capacity'] != 0
        load = status.pop('load')
        ship.set_load(load)
    equip_num = status.pop('equipnum')
    skill_list = status.pop('skill')
    ship.set_status(status=status)

    # 调用技能并写入
    skill_num = int(node.getAttribute('skill')) - 1
    sid = 'sid' + skill_list[skill_num]
    skill = getattr(skillCode, sid).skill  # 根据技能设置获取技能列表，未实例化
    ship.add_skill(skill)

    # 读取装备属性并写入
    assert equip_num == len(node.getElementsByTagName('Equipment'))
    for i in range(equip_num):
        e_node = node.getElementsByTagName('Equipment')[i]
        # TODO 如果装备也存在特殊效果，当作技能写入舰船skill内

    return ship
