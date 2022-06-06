# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import xml.dom.minidom

from src.utils import battleUtil
from src.wsgr.ship import *
import src.wsgr.ship as rship
import src.wsgr.equipment as requip
from src import skillCode


def load_config(config, dataset, timer):
    """加载配置文件"""
    dom = xml.dom.minidom.parse(config)
    root = dom.documentElement

    friend_root = root.getElementsByTagName('Fleet')[0]
    friend = load_fleet(friend_root, dataset, timer)

    # 根据战斗类型调用不同流程类
    battle_type = root.getAttribute('type')
    if battle_type != 'Map':
        try:
            battle = getattr(battleUtil, battle_type)
        except:
            raise ValueError(f'Battle type {battle_type} is not defined!')

        enemy_root = root.getElementsByTagName('Fleet')[1]
        enemy = load_fleet(enemy_root, dataset, timer)
        return battle(timer, friend, enemy)
    else:
        map_root = root.getElementsByTagName('Map')[0]
        mapid = map_root.getAttribute('mapid')


def load_fleet(node, dataset, timer):
    fleet = Fleet(timer)
    fleet.set_form(int(node.getAttribute('form')))

    shiplist = []
    for i in range(len(node.getElementsByTagName('Ship'))):
        s_node = node.getElementsByTagName('Ship')[i]
        ship = load_ship(s_node, dataset, timer)
        ship.set_master(fleet)
        shiplist.append(ship)

    fleet.set_ship(shiplist)
    fleet.set_side(int(node.getAttribute('side')))
    return fleet


def load_ship(node, dataset, timer):
    cid = node.getAttribute('cid')
    if cid[0] == '1':
        return load_friend_ship(node, dataset, timer)
    else:
        return load_enemy_ship(node, dataset, timer)


def load_friend_ship(node, dataset, timer):
    # 读取舰船属性
    cid = node.getAttribute('cid')
    status = dataset.get_friend_ship_status(cid)

    # 舰船对象实例化
    ship_type = status.pop('type')
    ship = getattr(rship, ship_type)(timer)  # 根据船型获取类，并实例化
    ship.set_cid(cid)

    # 写入节点属性
    ship.set_loc(int(node.getAttribute('loc')))
    ship.set_level(int(node.getAttribute('level')))
    ship.set_affection(int(node.getAttribute('affection')))

    if status['capacity'] != 0:
        load = status.pop('load')
        ship.set_load(load)
    equip_num = status.pop('equipnum')
    skill_list = status.pop('skill')

    if ship.affection > 100:  # 婚舰幸运+5
        status['luck'] += 5

    # 写入舰船属性
    ship.set_status(status=status)
    del status

    # 调用技能并写入
    skill_num = int(node.getAttribute('skill')) - 1
    if skill_num >= 0:
        sid = skill_list[skill_num]
    else:
        sid = ''
    if sid != '':
        sid = 'sid' + sid
        skill = getattr(skillCode, sid).skill  # 根据技能设置获取技能列表，未实例化
        ship.add_skill(skill)
        del skill

    # 读取装备属性并写入
    enodes = node.getElementsByTagName('Equipment')
    for i in range(len(enodes)):
        e_node = enodes[i]
        enum = int(e_node.getAttribute('loc'))
        if enum > equip_num:  # 装备所在栏位超出舰船装备限制
            continue

        equip = load_equip(e_node, dataset, ship, timer)
        ship.set_equipment(equip)

    return ship


def load_enemy_ship(node, dataset, timer):
    # 读取舰船属性
    cid = node.getAttribute('cid')
    status = dataset.get_enemy_ship_status(cid)

    # 舰船对象实例化
    ship_type = status.pop('type')
    ship = getattr(rship, ship_type)(timer)  # 根据船型获取类，并实例化
    ship.set_cid(cid)

    # 写入节点属性
    ship.set_loc(int(node.getAttribute('loc')))
    ship.set_level(int(node.getAttribute('level')))
    ship.set_affection(int(node.getAttribute('affection')))

    if status['capacity'] != 0:
        load = status.pop('load')
        ship.set_load(load)
    eid_list = status.pop('equip')
    skill_list = status.pop('skill')

    # 写入舰船属性
    ship.set_status(status=status)
    del status

    # 调用技能并写入
    # skill_num = int(node.getAttribute('skill')) - 1
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


def load_equip(node, dataset, master, timer):
    # 读取装备属性
    eid = node.getAttribute('eid')
    status = dataset.get_equip_status(eid)

    # 装备对象实例化
    equip_type = status.pop('type')
    enum = int(node.getAttribute('loc'))
    equip = getattr(requip, equip_type)(timer, master, enum)  # 根据装备类型获取类，并实例化

    # 如果装备也存在特殊效果，写入装备skill内
    esid = status.pop('skill')
    if esid != '':
        esid = 'esid' + esid
        skill = getattr(skillCode, esid).skill  # 根据技能设置获取技能列表，未实例化
        equip.add_skill(skill)  # 写入装备技能

    # 写入装备属性
    equip.set_status(status=status)

    return equip
