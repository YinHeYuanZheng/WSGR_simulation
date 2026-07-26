# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import os
import re
import xml.dom.minidom
import yaml

from src.utils import battleUtil
from src.utils.battleUtil import BattleUtil
from src.utils.mapUtil import MapUtil
from src.utils.parseEquipSkill import load_equip_config
import src.wsgr.ship as rship
import src.wsgr.equipment as requip
from src import skillCode


# A map id is also part of the standalone map filename.  Keep ordinary names
# (including Chinese and spaces) intact, while rejecting path traversal and
# characters that cannot be used in a filename on Windows.
INVALID_MAP_ID_PATTERN = re.compile(r'[<>:"/\\|?*\x00-\x1f]')


def map_yaml_path(mapid: str, mapDir: str) -> str:
    """Return the canonical standalone YAML path for a map id."""
    normalized = str(mapid).strip()
    if normalized in {'.', '..'} or INVALID_MAP_ID_PATTERN.search(normalized) \
            or normalized.endswith(('.', ' ')):
        raise ValueError(f'Invalid mapid: {mapid!r}')
    return os.path.join(mapDir, f'{normalized}.yaml')


def load_map_yaml(mapid: str, mapDir: str) -> dict:
    """Load a standalone map document containing nodes, routes and fleets."""
    map_file = map_yaml_path(mapid, mapDir)
    if not os.path.exists(map_file):
        raise FileNotFoundError(f"Map file '{map_file}' not found!")
    with open(map_file, 'r', encoding='utf-8') as file:
        map_config = yaml.safe_load(file)
    if not isinstance(map_config, dict):
        raise ValueError(f"Map file '{map_file}' must contain an object")
    file_mapid = str(map_config.get('mapid', '')).strip()
    if file_mapid != str(mapid).strip():
        raise ValueError(
            f"Map file '{map_file}' declares mapid {file_mapid!r}, "
            f"expected {str(mapid).strip()!r}"
        )
    if not isinstance(map_config.get('nodes'), list) or \
            not isinstance(map_config.get('routes'), list):
        raise ValueError(f"Map file '{map_file}' must contain nodes and routes")
    return map_config


def load_xml(infile: str, mapDir: str) -> dict:
    """xml to dict"""
    dom = xml.dom.minidom.parse(infile)
    root = dom.documentElement
    battle_type = root.getAttribute('type')

    # 检查战斗类型是否合法
    if battle_type != 'Map':
        try:
            getattr(battleUtil, battle_type)
        except:
            raise ValueError(f'Battle type {battle_type} is not defined!')
    else:
        map_root = root.getElementsByTagName('Map')[0]
        mapid = map_root.getAttribute('mapid')
        map_xml = os.path.join(mapDir, 'mapid' + mapid + '.xml')
        if not os.path.exists(map_xml):
            raise FileNotFoundError(f"Map file '{map_xml}' not found!")
    battleConfig = {'battle_type': battle_type}

    # 加载友方舰队
    friend_node = root.getElementsByTagName('Fleet')[0]
    friendDict = {'side': 1,
                  'form': int(friend_node.getAttribute('form'))}
    friendShipList = []
    for s_node in friend_node.getElementsByTagName('Ship'):
        shipDict = {
            'loc': int(s_node.getAttribute('loc')),
            'cid': s_node.getAttribute('cid'),
            'level': int(s_node.getAttribute('level')),
            'affection': int(s_node.getAttribute('affection')),
            'skill': int(s_node.getAttribute('skill')),
            'equipment': [
                {'loc': int(e_node.getAttribute('loc')),
                 'eid': e_node.getAttribute('eid')}
                for e_node in s_node.getElementsByTagName('Equipment')
            ],
            'strategy': [
                {'stid': st_node.getAttribute('stid'),
                 'level': int(st_node.getAttribute('level'))
                          if st_node.getAttribute('level') else 3}
                for st_node in s_node.getElementsByTagName('Strategy')
            ]
        }
        friendShipList.append(shipDict)
    friendDict['ships'] = friendShipList
    battleConfig['friend_fleet'] = friendDict

    # 加载敌方舰队/地图
    if battle_type != 'Map':
        try:
            enemy_node = root.getElementsByTagName('Fleet')[1]
        except:
            raise IndexError(f'Config type {battle_type}, but no enemy fleet detected')
        enemyDict = {'side': 0,
                     'form': int(enemy_node.getAttribute('form'))}
        enemyShipList = []
        for s_node in enemy_node.getElementsByTagName('Ship'):
            shipDict = {
                'loc': int(s_node.getAttribute('loc')),
                'cid': f"{s_node.getAttribute('cid')}",
                'level': int(s_node.getAttribute('level')),
                'affection': int(s_node.getAttribute('affection')),
                'skill': int(s_node.getAttribute('skill'))
            }
            enemyShipList.append(shipDict)
        enemyDict['ships'] = enemyShipList
        battleConfig['enemy_fleet'] = enemyDict
    else:
        map_root = root.getElementsByTagName('Map')[0]
        mapid = map_root.getAttribute('mapid')
        battleConfig['map'] = {'mapid': mapid,
                               'entrance': int(map_root.getAttribute('entrance')),
                               '_format': 'xml'}

    return battleConfig


def load_yaml(infile: str, mapDir: str) -> dict:
    """yaml to dict"""
    with open(infile, 'r') as f:
        battleConfig = yaml.safe_load(f)

    try:
        battle_type = battleConfig['battle_type']
    except KeyError:
        raise KeyError('Battle type is not defined!')
    try:
        battleConfig['friend_fleet']
    except KeyError:
        raise KeyError('Friend fleet is not defined!')

    if battle_type != 'Map':
        try:
            getattr(battleUtil, battle_type)  # battle
        except:
            raise ValueError(f'Battle type {battle_type} is not defined!')
        try:
            battleConfig['enemy_fleet']  # enemyDict
        except:
            raise ValueError(f'Config type {battle_type}, but no enemy fleet detected')
    else:
        map_config = battleConfig.get('map')
        if not isinstance(map_config, dict):
            raise ValueError('Map config is not defined!')
        mapid = str(map_config.get('mapid', '')).strip()
        if not mapid:
            raise ValueError('Map config must define mapid!')
        load_map_yaml(mapid, mapDir)

    return battleConfig


def load_config(battleConfig, mapDir, dataset, timer, log_func=print) -> BattleUtil or MapUtil:
    """加载战斗配置"""
    friendDict = battleConfig['friend_fleet']
    friend = load_fleet(friendDict, dataset, timer, log_func=log_func)

    # 根据战斗类型调用不同流程类
    battle_type = battleConfig['battle_type']
    if battle_type != 'Map':
        battle = getattr(battleUtil, battle_type)

        enemyDict = battleConfig['enemy_fleet']
        enemy = load_fleet(enemyDict, dataset, timer, log_func=log_func)
        if battle_type == 'CustomBattle':
            return battle(timer, friend, enemy, battleConfig.get('custom_phases'))
        return battle(timer, friend, enemy)
    else:
        mapDict = battleConfig['map']
        battle_map = load_map(
            mapDict, mapDir, dataset, timer, friend,
            map_document=battleConfig.get('_map_document'),
            enemy_ship_loader=load_enemy_ship,
            log_func=log_func,
        )
        return battle_map


def load_fleet(fleetDict, dataset, timer, log_func=print):
    fleet = rship.Fleet(timer)
    fleet.set_form(int(fleetDict['form']))

    shipList = []
    for shipDict in fleetDict['ships']:
        ship = load_ship(shipDict, dataset, timer, log_func=log_func)
        ship.set_master(fleet)
        shipList.append(ship)

    fleet.set_ship(shipList)
    fleet.set_side(int(fleetDict['side']))
    return fleet


def load_map(
        mapDict, mapDir, dataset, timer, friend, map_document=None,
        enemy_ship_loader=None, log_func=print,
):
    mapid = str(mapDict['mapid']).strip()
    map_yaml = map_yaml_path(mapid, mapDir)
    if map_document is not None:
        if not isinstance(map_document, dict):
            raise ValueError('Temporary map document must be an object')
        document_mapid = str(map_document.get('mapid', '')).strip()
        if document_mapid != mapid:
            raise ValueError(
                f'Temporary mapid {document_mapid!r} does not match config mapid {mapid!r}'
            )
        return MapUtil(
            timer, map_document, dataset, friend,
            enemy_ship_loader=enemy_ship_loader, log_func=log_func,
        )

    if mapDict.get('_format') != 'xml' and os.path.exists(map_yaml):
        return MapUtil(
            timer, load_map_yaml(mapid, mapDir), dataset, friend,
            enemy_ship_loader=enemy_ship_loader, log_func=log_func,
        )

    entrance_id = int(mapDict.get('entrance', 0))
    map_xml = os.path.join(mapDir, 'mapid'+mapid+'.xml')
    map_dom = xml.dom.minidom.parse(map_xml)
    root = map_dom.documentElement
    entrance = root.getElementsByTagName('entrance')[entrance_id]

    return MapUtil(timer, entrance, dataset, friend)


def load_ship(shipDict, dataset, timer, log_func=print):
    cid = shipDict['cid']
    if cid[0] == '1':
        return load_friend_ship(shipDict, dataset, timer, log_func=log_func)
    else:
        return load_enemy_ship(shipDict, dataset, timer, log_func=log_func)


def load_friend_ship(shipDict, dataset, timer, log_func=print):
    # 读取舰船属性
    cid = shipDict['cid']
    status = dataset.get_friend_ship_status(cid)

    # 舰船对象实例化
    ship_type = status.pop('type')
    ship = getattr(rship, ship_type)(timer)  # 根据船型获取类，并实例化
    ship.set_cid(cid)

    # 写入节点属性
    ship.set_loc(int(shipDict['loc']))
    ship.set_level(int(shipDict['level']))
    ship.set_affection(int(shipDict['affection']))

    # 写入非属性变量
    if status['capacity'] != 0:
        load = status.pop('load')
        ship.set_load(load)
    totalEquip = status.pop('equipnum')
    skillList = status.pop('skill')

    if ship.affection > 100:  # 婚舰幸运+5
        status['luck'] += 5

    # 写入舰船属性
    ship.set_status(status=status)
    del status

    # WebUI 可为友方舰船保存初始耐久。实际有效范围会在
    # Ship.init_health() 中根据技能、装备计算出的标准耐久再次截断。
    if 'input_health' in shipDict and shipDict['input_health'] is not None:
        ship.status['input_health'] = int(shipDict['input_health'])

    # 调用技能并写入
    skill_idx = int(shipDict['skill']) - 1
    sid = skillList[skill_idx] if skill_idx >= 0 else ''
    if sid != '':
        sid = 'sid' + sid
        skill = getattr(skillCode, sid).skill  # 根据技能设置获取技能列表，未实例化
        ship.add_skill(skill)
        del skill

    # 获取技能名称并输出
    try:
        skill_name = getattr(skillCode, sid).name
        log_func(f"{ship.status['name']} {skill_name}")
    except:
        log_func(f"{ship.status['name']} 未获取到技能名称")

    # 读取装备属性并写入
    for eDict in shipDict['equipment']:
        eLoc = int(eDict['loc'])
        if eLoc > totalEquip:  # 装备所在栏位超出舰船装备限制
            continue

        equip = load_equip(eDict, dataset, ship, timer)
        ship.set_equipment(equip)

    # 读取战术并写入
    for stDict in shipDict['strategy']:
        stid = 'stid' + stDict['stid']
        level = stDict['level']
        level = int(level) if level != '' else 3
        strategy = getattr(skillCode, stid).skill[0](timer, ship, level)
        ship.add_strategy(strategy)

    return ship


def load_enemy_ship(shipDict, dataset, timer, log_func=print):
    # 读取舰船属性
    cid = shipDict['cid']
    status = dataset.get_enemy_ship_status(cid)

    # 舰船对象实例化
    ship_type = status.pop('type')
    ship = getattr(rship, ship_type)(timer)  # 根据船型获取类，并实例化
    ship.set_cid(cid)

    # 写入节点属性
    ship.set_loc(int(shipDict['loc']))
    ship.set_affection(int(shipDict.get('affection', 50)))

    # 写入非属性变量
    dataset_level = status.pop('level')
    ship.set_level(int(shipDict.get('level', dataset_level)))
    if status['capacity'] != 0:
        load = status.pop('load')
        ship.set_load(load)
    eid_list = status.pop('equip')
    skill_list = status.pop('skill')

    # 写入舰船属性
    ship.set_status(status=status)
    del status

    # 调用技能并写入
    # skill_num = int(shipDict['skill']) - 1
    skill_num = 0  # 默认只有一个技能
    sid = skill_list[skill_num]
    if sid != '' and int(shipDict.get('skill', 1)) != 0:  # skill=0可用于去除敌舰技能
        sid = 'sid' + sid
        skill = getattr(skillCode, sid).skill  # 根据技能设置获取技能列表，未实例化
        ship.add_skill(skill)
        del skill

        # 获取技能名称并输出
        try:
            skill_name = getattr(skillCode, sid).name
            log_func(f"{ship.status['name']} {skill_name}")
        except:
            log_func(f"{ship.status['name']} 未获取到技能名称")

    # 读取装备属性并写入
    for i, eid in enumerate(eid_list):
        if eid != '':
            estatus = dataset.get_equip_status(eid)
            equip_type = estatus.pop('type')
            equip = getattr(requip, equip_type)(timer, ship, i + 1)  # 根据装备类型获取类，并实例化

            # 读取装备特效配置
            skill_config = estatus.pop('skill_config')
            if skill_config != '':
                equip.add_skill(load_equip_config(skill_config, eid))

            # 写入装备属性
            equip.set_status(status=estatus)
            ship.set_equipment(equip)

    return ship


def load_equip(equipDict, dataset, master, timer):
    # 读取装备属性
    eid = equipDict['eid']
    status = dataset.get_equip_status(eid)

    # 装备对象实例化
    equip_type = status.pop('type')
    enum = int(equipDict['loc'])
    equip = getattr(requip, equip_type)(timer, master, enum)  # 根据装备类型获取类，并实例化

    # 读取装备特效配置
    skill_config = status.pop('skill_config')
    if skill_config != '':
        equip.add_skill(load_equip_config(skill_config, eid))

    # 写入装备属性
    equip.set_status(status=status)

    return equip


if __name__ == '__main__':
    battleConfig = load_xml(r'D:\文件\战舰少女\WSGR_simulation\config\event\cv_simulation\config_37.xml',
                            r'D:\文件\战舰少女\WSGR_simulation\depend\map')
    # battleConfig = load_yaml(r'./config_37.yaml',
    #                          r'D:\文件\战舰少女\WSGR_simulation\depend\map')
    print(battleConfig)
    yaml.safe_dump(battleConfig, open(r'./config_37.yaml', 'w'), sort_keys=False)
