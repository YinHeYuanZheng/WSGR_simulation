# -*- coding:utf-8 -*-
# Author:银河远征
# env:py38

import re
import numpy as np

from src.wsgr.wsgrTimer import Time
from src.utils import battleUtil
from src.utils.parseEquipSkill import load_equip_config
import src.wsgr.ship as rship
import src.wsgr.equipment as requip
from src import skillCode


RESOURCE_LABELS = {
    'oil': '燃油',
    'ammo': '弹药',
    'steel': '钢材',
    'almn': '铝材',
}
RESOURCE_KINDS = {'resource_gain': -1, 'resource_loss': 1}


class UserRules:
    """地图出征时由用户 YAML 配置的决策规则。"""

    _DEFAULTS = {
        'formation': 2,
        'formation_if_recon_fails': False,
        'long_missile': False,
        'night': False,
        'round': True,
        'rules': [],
        'retreat_if_recon_fails': False,
        'retreat_if_round_fails': True,
        'proceed': True,
        'proceed_stop': [2, 2, 2, 2, 2, 2],
    }
    _CONDITION_PATTERN = re.compile(
        r'^\(\s*([A-Za-z_]\w*)\s*(>=|<=|==|!=|>|<)\s*(\d+)\s*\)$'
    )

    def __init__(self, config, node_names):
        if not isinstance(config, dict):
            raise ValueError('User rules must be a YAML object')
        if 'selected_nodes' not in config:
            raise ValueError('Map user rules must define selected_nodes')

        selected_nodes = config['selected_nodes']
        if selected_nodes == 'all':
            self.selected_nodes = None
        elif isinstance(selected_nodes, list) and all(
                isinstance(name, str) and name.strip() for name in selected_nodes):
            self.selected_nodes = {name.strip() for name in selected_nodes}
            unknown = self.selected_nodes - set(node_names)
            if unknown:
                raise ValueError(f'Unknown selected map node(s): {sorted(unknown)}')
        else:
            raise ValueError("selected_nodes must be 'all' or a list of node names")

        raw_defaults = config.get('node_defaults', {})
        self.defaults = self._make_settings(raw_defaults, 'node_defaults')
        raw_node_args = config.get('node_args', {})
        if not isinstance(raw_node_args, dict):
            raise ValueError('node_args must be an object')
        unknown = set(raw_node_args) - set(node_names)
        if unknown:
            raise ValueError(f'Unknown node_args node(s): {sorted(unknown)}')
        self.node_args = {
            name: self._make_settings(values, f'node_args.{name}', self.defaults)
            for name, values in raw_node_args.items()
        }

    def _make_settings(self, values, location, base=None):
        if not isinstance(values, dict):
            raise ValueError(f'{location} must be an object')
        values = dict(values)
        if 'enemy_rules' in values:
            if 'rules' in values:
                raise ValueError(f'{location} cannot define both rules and enemy_rules')
            values['rules'] = values.pop('enemy_rules')
        has_rule_override = 'rules' in values
        unknown = set(values) - set(self._DEFAULTS)
        if unknown:
            raise ValueError(f'{location} contains unsupported field(s): {sorted(unknown)}')
        settings = dict(self._DEFAULTS if base is None else base)
        settings.update(values)

        settings['formation'] = self._validate_formation(
            settings['formation'], f'{location}.formation'
        )
        failed_formation = settings['formation_if_recon_fails']
        if failed_formation is not False:
            settings['formation_if_recon_fails'] = self._validate_formation(
                failed_formation, f'{location}.formation_if_recon_fails'
            )
        if settings['night'] not in {True, False, 'flag_alive'}:
            raise ValueError(f'{location}.night must be True, False, or flag_alive')
        if isinstance(settings['round'], bool):
            pass
        elif isinstance(settings['round'], (int, float)) and 0 <= settings['round'] <= 100:
            pass
        else:
            raise ValueError(f'{location}.round must be a boolean or a number from 0 to 100')
        for field in (
                'long_missile', 'retreat_if_recon_fails',
                'retreat_if_round_fails', 'proceed'):
            if not isinstance(settings[field], bool):
                raise ValueError(f'{location}.{field} must be a boolean')
        stop = settings['proceed_stop']
        if not isinstance(stop, list) or len(stop) != 6 or \
                any(value not in {-1, 1, 2} for value in stop):
            raise ValueError(
                f'{location}.proceed_stop must contain six values chosen from -1, 1, 2'
            )
        if base is None or has_rule_override:
            settings['rules'] = self._parse_rules(settings['rules'], f'{location}.rules')
        return settings

    @staticmethod
    def _validate_formation(value, location):
        if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= 5:
            raise ValueError(f'{location} must be an integer from 1 to 5')
        return value

    def _parse_rules(self, rules, location):
        if rules is None:
            return []
        if not isinstance(rules, list):
            raise ValueError(f'{location} must be a list')
        parsed_rules = []
        for index, rule in enumerate(rules):
            if not isinstance(rule, list) or len(rule) != 2:
                raise ValueError(f'{location}[{index}] must be [condition, action]')
            condition, action = rule
            if not isinstance(condition, str):
                raise ValueError(f'{location}[{index}][0] must be a string')
            self._validate_condition(condition, f'{location}[{index}][0]')
            if isinstance(action, str) and action in {'retreat', 'round'}:
                parsed_action = action
            else:
                parsed_action = self._validate_formation(
                    int(action) if isinstance(action, str) and action.isdigit() else action,
                    f'{location}[{index}][1]',
                )
            parsed_rules.append((condition, parsed_action))
        return parsed_rules

    def _validate_condition(self, expression, location):
        for or_part in re.split(r'\s+or\s+', expression.strip()):
            and_parts = re.split(r'\s+and\s+', or_part)
            if not and_parts or any(not part for part in and_parts):
                raise ValueError(f'Invalid rule condition at {location}: {expression!r}')
            for part in and_parts:
                match = self._CONDITION_PATTERN.fullmatch(part.strip())
                if match is None:
                    raise ValueError(f'Invalid rule condition at {location}: {expression!r}')
                ship_type = getattr(rship, match.group(1), None)
                if not isinstance(ship_type, type) or not issubclass(ship_type, rship.Ship):
                    raise ValueError(f'Unknown ship type {match.group(1)!r} at {location}')

    def settings_for(self, point):
        return self.node_args.get(point.name, self.defaults)

    def is_selected(self, point):
        return point.type is battleUtil.Entrance or self.selected_nodes is None \
            or point.name in self.selected_nodes

    def select_initial_formation(self, point, friend):
        friend.set_form(self.settings_for(point)['formation'])

    def apply_recon_decision(self, point, friend, enemy, timer):
        settings = self.settings_for(point)
        if not timer.recon_flag:
            formation = settings['formation_if_recon_fails']
            if formation is not False:
                friend.set_form(formation)
            if settings['retreat_if_recon_fails']:
                timer.map_retreat = True
                timer.info('【策略】索敌失败，撤退\n')
            return

        for condition, action in settings['rules']:
            if self._condition_matches(condition, enemy):
                if action == 'retreat':
                    timer.map_retreat = True
                    timer.info(f'【策略】{condition}，撤退\n')
                elif action == 'round':
                    point.round_request = True
                    timer.info(f'【策略】{condition}，尝试迂回\n')
                else:
                    assert action in {1, 2, 3, 4, 5}
                    friend.set_form(action)
                    timer.info(f'【策略】{condition}，选择阵型 {action}\n')
                return

    def _condition_matches(self, expression, enemy):
        return any(
            all(self._single_condition_matches(part.strip(), enemy)
                for part in re.split(r'\s+and\s+', or_part))
            for or_part in re.split(r'\s+or\s+', expression.strip())
        )

    def _single_condition_matches(self, condition, enemy):
        ship_name, operator, value = self._CONDITION_PATTERN.fullmatch(condition).groups()
        ship_type = getattr(rship, ship_name)
        count = sum(isinstance(ship, ship_type) for ship in enemy.ship)
        value = int(value)
        return {
            '>=': count >= value, '<=': count <= value, '>': count > value,
            '<': count < value, '==': count == value, '!=': count != value,
        }[operator]

    def should_attempt_round(self, point, round_rate):
        request = point.round_request
        if not point.can_roundabout or request is False or request is None:
            return False
        if isinstance(request, bool):
            return request
        return round_rate * 100 > request

    def should_retreat_if_round_failure(self, point):
        return self.settings_for(point)['retreat_if_round_fails']

    def should_run_night(self, point, enemy):
        value = self.settings_for(point)['night']
        if value == 'flag_alive':
            return bool(enemy.ship) and enemy.ship[0].damaged != 4
        return value

    def should_run_long_missile(self, point):
        return self.settings_for(point)['long_missile']

    def should_proceed(self, point, friend):
        settings = self.settings_for(point)
        if not settings['proceed']:
            return False
        for ship in friend.ship:
            threshold = settings['proceed_stop'][ship.loc - 1]
            if threshold != -1 and ship.damaged >= threshold + 1:
                return False
        return True


class DefaultUserRules(UserRules):
    """未配置用户策略时保持历史地图模拟行为。"""

    def __init__(self, node_names):
        self.selected_nodes = None
        self.node_args = {}
        self.defaults = dict(self._DEFAULTS)

    def select_initial_formation(self, point, friend):
        friend.set_form(4 if point.level == 5 else 2)

    def should_proceed(self, point, friend):
        return all(ship.loc != 1 or ship.damaged < 3 for ship in friend.ship)

    def should_retreat_if_round_failure(self, point):
        return False

    def should_run_night(self, point, enemy):
        return point.level == 5

    def should_run_long_missile(self, point):
        return True


class MapUtil(Time):
    """地图调用基类"""

    def __init__(self, timer, map_config, dataset, friend, user_rules=None, log_func=print):
        super().__init__(timer)
        self.friend = friend
        self.point = {}
        self.map_config = map_config
        self.log_func = log_func
        self.entrance_name = 'entrance'
        self.init_map(map_config, dataset)
        self.user_rules = UserRules(user_rules, self.point) \
            if user_rules is not None else DefaultUserRules(self.point)
        for point in self.point.values():
            point.set_user_rules(self.user_rules)

    def init_map(self, map_config, dataset):
        """根据传入的字典结构和数据库，构建海图"""
        if not isinstance(map_config, dict):
            raise TypeError('Map configuration must be an object')
        nodes = map_config.get('nodes')
        routes = map_config.get('routes')
        if not isinstance(nodes, list) or not nodes:
            raise ValueError('Map nodes must be a non-empty list')
        if not isinstance(routes, list):
            raise ValueError('Map routes must be a list')

        names = set()
        for node in nodes:
            if not isinstance(node, dict):
                raise ValueError('Each map node must be an object')
            name = str(node.get('name', '')).strip()
            if not name:
                raise ValueError('Map node name cannot be empty')
            if name in names:
                raise ValueError(f'Duplicate map node name: {name}')
            names.add(name)

            level = int(node.get('level', 2))
            battle_config = node.get('battle') or {}
            battle_type = str(battle_config.get('type', 'NormalBattle'))
            if battle_type not in {
                    'Entrance', 'MidPoint', 'ResourcePoint', 'NormalBattle', 'AirBattle', 'NightBattle'}:
                raise ValueError(f'Unsupported map battle type: {battle_type}')

            kind = str(node.get('kind', ''))
            is_resource_point = battle_type == 'ResourcePoint'
            if is_resource_point != (kind in RESOURCE_KINDS):
                raise ValueError(
                    f'Point {name} must use kind resource_gain/resource_loss with ResourcePoint'
                )

            point = Point(name, level)
            point.set_type(getattr(battleUtil, battle_type))
            point.set_roundabout(bool(battle_config.get('roundabout', False)))
            point.set_support(bool(battle_config.get('support', False)))
            if is_resource_point:
                resource_key = str(battle_config.get('resource', '')).strip()
                if resource_key not in RESOURCE_LABELS:
                    raise ValueError(f'Point {name} has an unsupported resource type')
                amount = battle_config.get('amount')
                if isinstance(amount, bool) or not isinstance(amount, int) or amount < 0:
                    raise ValueError(f'Point {name} resource amount must be a non-negative integer')
                point.set_resource_change(
                    resource_key, RESOURCE_KINDS[kind] * amount, RESOURCE_LABELS[resource_key],
                )

            enemy_list = []
            for fleet_config in node.get('enemy_fleets') or []:
                enemy_list.append(self.load_fleet(fleet_config, dataset, self.timer))
            if battle_type in {'Entrance', 'MidPoint', 'ResourcePoint'} and enemy_list:
                raise ValueError(f'Non-combat point {name} cannot contain enemy fleets')
            if battle_type not in {'Entrance', 'MidPoint', 'ResourcePoint'} and not enemy_list:
                raise ValueError(f'Combat point {name} must contain at least one enemy fleet')
            point.set_enemy(enemy_list)
            point.set_suc({})
            self.point[name] = point

            if battle_type == 'Entrance':
                if self.entrance_name != 'entrance' and self.entrance_name != name:
                    raise ValueError('Map must contain exactly one entrance point')
                self.entrance_name = name

        entrance_nodes = [
            node for node in nodes
            if str((node.get('battle') or {}).get('type')) == 'Entrance'
        ]
        if len(entrance_nodes) != 1:
            raise ValueError('Map must contain exactly one entrance point')

        for route in routes:
            if not isinstance(route, dict):
                raise ValueError('Each map route must be an object')
            source = str(route.get('from', '')).strip()
            target = str(route.get('to', '')).strip()
            if source not in self.point or target not in self.point:
                raise ValueError(f'Map route references an unknown point: {source} -> {target}')
            if source == target:
                raise ValueError(f'Map route cannot point to itself: {source}')
            if target in self.point[source].suc:
                raise ValueError(f'Duplicate map route: {source} -> {target}')
            requests = [
                LeadRequest(
                    request_type=str(condition.get('type', '')),
                    name=str(condition.get('name', '')),
                    fun=str(condition.get('fun', '')),
                    value=condition.get('value', ''),
                )
                for condition in (route.get('conditions') or [])
            ]
            relation = 'or' if route.get('relation') in {'or', 'any'} else 'and'
            self.point[source].suc[target] = Successor(
                float(route.get('weight', 1)), requests, relation
            )

        for name, point in self.point.items():
            if point.level in [0, 1, 2, 3] and not point.suc:
                raise ValueError(f'Point {name} should have successor(s)!')
            if not point.suc and point.level not in [4, 5]:
                raise ValueError(f'Terminal point {name} must have level 4 or 5')

    def load_fleet(self, fleet_config, dataset, timer):
        """Load one enemy fleet from the normalized map document."""
        if not isinstance(fleet_config, dict):
            raise ValueError('Enemy fleet must be an object')
        fleet = rship.Fleet(timer)
        fleet.set_form(int(fleet_config.get('formation', fleet_config.get('form', 1))))

        shiplist = []
        for index, ship_config in enumerate(fleet_config.get('ships') or []):
            cid = str(ship_config.get('cid', '')).strip()
            if not cid:
                raise ValueError('Enemy ship cid cannot be empty')
            normalized_ship = {
                'loc': int(ship_config.get('loc', index + 1)),
                'cid': cid,
                'level': int(ship_config.get('level', 1)),
                'affection': int(ship_config.get('affection', 50)),
                'skill': int(ship_config.get('skill', 1)),
            }
            ship = self.load_enemy_ship(normalized_ship, dataset, timer)
            ship.set_master(fleet)
            shiplist.append(ship)
        if not shiplist:
            raise ValueError('Enemy fleet cannot be empty')
        if len(shiplist) > 6:
            raise ValueError('Enemy fleet cannot contain more than 6 ships')
        fleet.set_ship(shiplist)
        fleet.set_side(0)
        return fleet

    def load_enemy_ship(self, ship_config, dataset, timer):
        from src.utils.loadConfig import load_enemy_ship
        return load_enemy_ship(ship_config, dataset, timer, log_func=self.log_func)

    def start(self):
        name = self.entrance_name
        path = []
        self.timer.report_log('map_battles', [])
        self.timer.report_log('map_node_events', [])
        while name is not None:
            point = self.point[name]
            path.append(name)
            name = point.start(self.timer, self.friend)
        self.timer.report_log('map_path', path)
        self.timer.report_log(
            'map_battle_count',
            len(self.timer.log['map_battles']),
        )

    def report(self):
        # 消耗
        supply = self.timer.log['supply']
        for tmp_ship in self.friend.ship:
            ship_supply = tmp_ship.reset()
            supply['oil'] += int(ship_supply['oil'])
            supply['ammo'] += int(ship_supply['ammo'])
            supply['steel'] += int(ship_supply['steel'])
            supply['almn'] += int(ship_supply['almn'])
            supply['repeat'] += int(ship_supply['repeat'])
        self.timer.report_log('supply', supply)

        return self.timer.log


class Point:
    """节点基类"""

    def __init__(self, name, level):
        self.name = name
        self.level = level  # 节点等级, 0: 起点, 1: 出门, 2: 道中, 3: 门神, 4: 非boss地图终点, 5: boss
        self.type = None
        self.can_roundabout = False
        self.round_request = None
        self.support = False
        self.resource_key = None
        self.resource_delta = 0
        self.resource_label = ''
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
        self.can_roundabout = bool(roundabout)

    def set_user_rules(self, user_rules):
        self.user_rules = user_rules

    def set_support(self, support):
        self.support = bool(support)

    def set_resource_change(self, resource_key, resource_delta, resource_label):
        self.resource_key = resource_key
        self.resource_delta = int(resource_delta)
        self.resource_label = resource_label

    def set_enemy(self, enemy_list):
        self.enemy_list = enemy_list

    def set_suc(self, suc_dic):
        self.suc = suc_dic

    def start(self, timer, friend):
        """创建战斗类并移动到下个点"""
        timer.set_point(self)
        timer.map_retreat = False
        self.round_request = self.user_rules.settings_for(self)['round']
        if not self.user_rules.is_selected(self):
            timer.map_retreat = True
            timer.log['end_with'] = self.name
            timer.info('【策略】到达未选择节点，撤退\n')
            return None

        self.user_rules.select_initial_formation(self, friend)

        if len(self.enemy_list) != 0:
            enemy = np.random.choice(self.enemy_list)
            self.battle = self.type(timer, friend, enemy)
        else:
            from src.wsgr.ship import Fleet
            enemy = Fleet(timer)
            self.battle = self.type(timer, friend, enemy)
        self.battle.start()
        if self.type not in {battleUtil.Entrance, battleUtil.MidPoint, battleUtil.ResourcePoint}:
            timer.log['map_node_events'].append({
                'name': self.name,
                'recon_rate': timer.log['recon'][0],
                'roundabout_rate': timer.log['round'][0] if self.can_roundabout else None,
            })
        if self.type not in {battleUtil.Entrance, battleUtil.MidPoint, battleUtil.ResourcePoint} and \
                not timer.map_retreat and not timer.round_flag:
            final_state = np.asarray(timer.log['damaged_state'])[-1]
            friend_state = final_state[:len(friend.ship)].astype(int).tolist()
            enemy_state = final_state[6:6 + len(enemy.ship)].astype(int).tolist()
            timer.log['map_battles'].append({
                'name': self.name,
                'result': str(timer.log.get('result', '')),
                'friend_damaged_state': friend_state,
                'boss': self.level == 5,
                'boss_flagship_sunk': bool(enemy_state and enemy_state[0] == 4),
            })
        return self.move(friend)

    def move(self, friend):
        self.battle.timer.log['end_with'] = self.name
        if self.battle.timer.map_retreat:
            return None
        # 地图终点
        if not len(self.suc):
            assert self.level in [4, 5]
            if self.level == 5:
                self.battle.timer.log['end_with_boss'] = True
            return None

        if not self.user_rules.should_proceed(self, friend):
            return None
        for tmp_ship in friend.ship:
            # 油弹耗尽不再前进
            if tmp_ship.supply_oil <= 0 or tmp_ship.supply_ammo <= 0:
                return None

        # 带路检定
        for name, suc_point in sorted(self.suc.items(), key=lambda item: item[0]):
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
