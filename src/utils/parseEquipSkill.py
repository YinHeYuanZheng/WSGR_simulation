# -*- coding:utf-8 -*-
"""将装备数据库“特效配置”单元格转换为 EquipSkill 类。

配置语法速查：
    hit_rate:0.1                       普通词条，使用默认阶段
    hit_rate:0.1,AirPhase              普通词条，覆盖生效阶段
    entry1;entry2                      同一层级的多个配置项
    {crit:0.1;hit_rate:0.05}           合并为一个技能的最终词条组
    Cid(533,{crit:0.1;hit_rate:0.05})  包装并合并最终词条组
    Country(C,ShipType(CLT,{...}))     包装器嵌套，不使用大括号
    pierce_coef:0.05,stack             覆盖特殊不叠加规则
    pierce_coef:0.05,stack,ShellingPhase
    @013:0.1                           定向调用现有 Python 装备技能

解析器只负责有限的声明式语法，不执行单元格中的任意 Python 表达式。
无法通过注册词条和包装器表达的技能应继续使用 @esid 定向。
"""

import importlib
import json
import re

import src.wsgr.phase as rphase
import src.wsgr.ship as rship
from src.wsgr.skill import EquipEffect, EquipSkill, SelfTarget, Target


# 普通词条注册表。phase 和 bias_or_weight 对应现有 Buff 接口；
# effect_type=3/4 沿用 Ship.add_buff 中“同类取最高值”的特殊规则。
EFFECT_REGISTRY = {
    'pierce_coef': {'phase': 'AllPhase', 'bias_or_weight': 0, 'effect_type': 3},
    'uplimit_buff': {'phase': 'ShellingPhase', 'bias_or_weight': 0, 'effect_type': 4},
    'hit_rate': {'phase': 'AllPhase', 'bias_or_weight': 0},
    'miss_rate': {'phase': 'AllPhase', 'bias_or_weight': 0},
    'crit': {'phase': 'AllPhase', 'bias_or_weight': 0},
    'power_buff': {'phase': 'AllPhase', 'bias_or_weight': 2},
    'final_damage_buff': {'phase': 'AllPhase', 'bias_or_weight': 2},
    'air_ctrl_buff': {'phase': 'AirPhase', 'bias_or_weight': 0},
    'air_atk_buff': {'phase': 'AirPhase', 'bias_or_weight': 2},
    'air_bomb_atk_buff': {'phase': 'AirPhase', 'bias_or_weight': 2},
    'air_dive_atk_buff': {'phase': 'AirPhase', 'bias_or_weight': 2},
}

# 条件和目标包装器会递归向内部叶子词条传递状态。
WRAPPER_NAMES = {'Cid', 'Country', 'Tag', 'ShipType', 'Side'}


class EquipConfigError(ValueError):
    """带装备编号和原始配置文本的装备特效配置错误。"""


class ConfigEffectType(int):
    """可比较的动态特效编号，调试输出格式为 ``eid.词条序号``。

    Ship.add_buff 需要将 effect_type 与数字 2/3/4 比较，因此这里继承
    int 保持现有判定兼容；数据库装备加载时同时保存 eid 作为可读标签。
    """

    def __new__(cls, eid, index):
        eid_text = str(eid)
        eid_value = int(eid_text) if eid_text.isdigit() else 0
        value = 100000000 + eid_value * 1000 + index
        instance = int.__new__(cls, value)
        instance.eid = eid_text
        instance.index = index
        return instance

    def __repr__(self):
        return f'{self.eid}.{self.index:03d}'

    __str__ = __repr__


def _split_top_level(text, delimiter):
    """仅在最外层切分文本，忽略括号、大括号、数组和引号内的分隔符。"""
    result = []
    start = 0
    stack = []
    quote = None
    escaped = False
    pairs = {')': '(', '}': '{', ']': '['}

    for index, char in enumerate(text):
        if quote is not None:
            if escaped:
                escaped = False
            elif char == '\\':
                escaped = True
            elif char == quote:
                quote = None
            continue

        if char in '"\'':
            quote = char
        elif char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack.pop() != pairs[char]:
                raise ValueError(f'装备特效配置括号不匹配: {text}')
        elif char == delimiter and not stack:
            result.append(text[start:index].strip())
            start = index + 1

    if quote is not None or stack:
        raise ValueError(f'装备特效配置括号或引号不完整: {text}')
    result.append(text[start:].strip())
    return [item for item in result if item]


def _parse_value(text):
    """解析 JSON 标量或数组；未加引号的接口名称保留为字符串。"""
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return text


def _normalize_cid(value):
    """规范化 Cid 包装器参数。

    三位编号代表友方舰船，自动展开为未改造 10xxx 和改造 11xxx；
    五位编号直接使用，可用于精确指定友方或敌方舰船。
    """
    values = value if isinstance(value, list) else [value]
    values = [str(item).zfill(3) for item in values]
    lengths = {len(item) for item in values}

    if len(lengths) != 1:
        raise ValueError('Cid 包装器不能混用三位和五位编号')
    if lengths == {3}:
        if not all(item.isdigit() for item in values):
            raise ValueError('三位 Cid 必须为数字')
        return [
            cid
            for item in values
            for cid in (f'10{item}', f'11{item}')
        ]
    if lengths == {5}:
        if not all(item.isdigit() and item[0] in ['0', '1'] for item in values):
            raise ValueError('五位 Cid 必须以 0 或 1 开头')
        return values
    raise ValueError('Cid 包装器只接受三位或五位编号')


def _parse_effect_group(text, conditions, side, require_multiple):
    """解析大括号中的最终普通词条组。

    两个及以上普通词条保留为 group，后续生成一个包含多个 EquipEffect
    的 EquipSkill。包装器使用大括号包裹单个词条时仍返回普通叶子。
    """
    raw_entries = _split_top_level(text, ';')
    if require_multiple and len(raw_entries) < 2:
        raise ValueError('顶层大括号必须包裹两个或更多普通词条')

    has_wrapper = any(
        re.fullmatch(r'[A-Z][A-Za-z0-9_]*\(.*\)', entry)
        for entry in raw_entries
    )
    has_effect = any(
        not re.fullmatch(r'[A-Z][A-Za-z0-9_]*\(.*\)', entry)
        for entry in raw_entries
    )
    if has_wrapper and has_effect:
        raise ValueError('大括号不可同时包裹普通词条和包装器')
    if has_wrapper:
        return _parse_entries(text, conditions, side)
    if len(raw_entries) == 1 and raw_entries[0].startswith('@'):
        return _parse_entries(text, conditions, side)

    entries = _parse_entries(text, conditions, side)
    if any(entry['kind'] != 'effect' for entry in entries):
        raise ValueError('合并技能的大括号只能包裹普通词条')
    if len(entries) < 2:
        return entries
    return [{'kind': 'group', 'entries': entries}]


def _parse_entries(text, conditions=None, side=None):
    """递归解析配置，最终展开为互相独立的叶子词条。

    conditions 和 side 是包装器向内部传递的上下文。最终
    返回的每个字典均可独立生成一个动态 EquipSkill：
        kind='effect'  普通注册词条
        kind='python'  @esid Python 定向
    """
    conditions = [] if conditions is None else conditions
    entries = []

    for entry in _split_top_level(text, ';'):
        if entry.startswith('{') and entry.endswith('}'):
            entries.extend(_parse_effect_group(
                entry[1:-1], conditions, side,
                require_multiple=True
            ))
            continue

        wrapper = re.fullmatch(r'([A-Z][A-Za-z0-9_]*)\((.*)\)', entry)
        if wrapper:
            name, content = wrapper.groups()
            if name not in WRAPPER_NAMES:
                raise ValueError(f'未知装备特效包装器: {name}')
            args = _split_top_level(content, ',')
            if len(args) != 2:
                raise ValueError(f'{name} 包装器必须填写条件和被包装内容两个参数')
            value = _parse_value(args[0])
            wrapped = args[1]
            # 大括号明确表示一组配置项；包装器本身已经是完整配置项，
            # 因此包装器嵌套时不再额外使用大括号。
            if wrapped.startswith('{') and wrapped.endswith('}'):
                inner = wrapped[1:-1]
                parse_inner = lambda next_conditions, next_side: _parse_effect_group(
                    inner, next_conditions, next_side,
                    require_multiple=False
                )
            elif re.fullmatch(r'[A-Z][A-Za-z0-9_]*\(.*\)', wrapped):
                inner = wrapped
                parse_inner = lambda next_conditions, next_side: _parse_entries(
                    inner, next_conditions, next_side
                )
            else:
                raise ValueError(
                    f'{name} 包裹普通词条时必须使用大括号，'
                    '包裹包装器时直接填写包装器'
                )
            if name == 'Side':
                if value not in [0, 1]:
                    raise ValueError('Side 只能填写 0 或 1')
                entries.extend(parse_inner(conditions, value))
            else:
                if name == 'Cid':
                    value = _normalize_cid(value)
                entries.extend(parse_inner(conditions + [(name, value)], side))
            continue

        if entry.startswith('@'):
            # Python 定向保留原 esid 实现；包装器条件和目标仍可作用于它。
            match = re.fullmatch(r'@(?:esid)?(\d+)(?::(.*))?', entry)
            if match is None:
                raise ValueError(f'Python 装备特效定向格式错误: {entry}')
            values = []
            if match.group(2):
                values = [_parse_value(value) for value in _split_top_level(match.group(2), ',')]
            entries.append({
                'kind': 'python',
                'esid': match.group(1).zfill(3),
                'values': values,
                'conditions': conditions,
                'side': side,
            })
            continue

        # 其余配置项按普通词条 name:value[,phase] 解析。
        parts = _split_top_level(entry, ':')
        if len(parts) != 2:
            raise ValueError(f'普通装备特效格式错误: {entry}')
        name = parts[0]
        if name not in EFFECT_REGISTRY:
            raise ValueError(f'未知装备特效词条: {name}')
        args = _split_top_level(parts[1], ',')
        if not 1 <= len(args) <= 3:
            raise ValueError(f'{name} 最多只能填写数值、stack和阶段三个参数')
        stackable = len(args) >= 2 and args[1] == 'stack'
        if len(args) == 3 and not stackable:
            raise ValueError(f'{name} 的第二个参数必须为 stack')
        phase = args[2] if len(args) == 3 else (
            None if stackable else args[1] if len(args) == 2 else None
        )
        entries.append({
            'kind': 'effect',
            'name': name,
            'value': float(_parse_value(args[0])),
            'phase': phase,
            'conditions': conditions,
            'side': side,
            'stackable': stackable,
        })

    return entries


def parse_equip_config(config):
    """公开解析入口：将单元格配置解析为独立叶子词条。"""
    if not isinstance(config, str) or not config.strip():
        return []
    return _parse_entries(config.strip())


def _match_condition(master, name, value):
    """判断装备携带者是否满足一个条件包装器。"""
    values = value if isinstance(value, list) else [value]
    if name == 'Cid':
        return master.cid in values
    if name == 'Country':
        return master.status['country'] in values
    if name == 'Tag':
        return master.status['tag'] in values
    if name == 'ShipType':
        try:
            shiptypes = tuple(getattr(rship, item) for item in values)
        except AttributeError as exc:
            raise ValueError(f'未知舰种: {value}') from exc
        return isinstance(master, shiptypes)
    raise ValueError(f'未知装备特效条件: {name}')


def _conditions_active(master, conditions):
    return all(_match_condition(master, name, value) for name, value in conditions)


def _validate_entry(entry):
    """提前检查原本会延迟到技能实例化阶段才发现的配置错误。"""
    if entry['kind'] == 'group':
        for child in entry['entries']:
            _validate_entry(child)
        return
    if entry['kind'] != 'effect':
        return

    registry = EFFECT_REGISTRY[entry['name']]
    _phase(entry['phase'] or registry['phase'])
    for name, value in entry['conditions']:
        if name != 'ShipType':
            continue
        values = value if isinstance(value, list) else [value]
        try:
            for item in values:
                getattr(rship, item)
        except AttributeError as exc:
            raise ValueError(f'未知舰种: {value}') from exc


def _target(master, side):
    """未指定 Side 时作用于装备者；指定后作用于对应舰队全体。"""
    return SelfTarget(master) if side is None else Target(side=side)


def _phase(name):
    """将配置中的现有 Phase 类名转换为对应类。"""
    try:
        return getattr(rphase, name)
    except AttributeError as exc:
        raise ValueError(f'未知装备特效阶段: {name}') from exc


def _effect_buff(timer, entry, effect_type):
    """根据一个普通叶子词条创建 EquipEffect。"""
    registry = EFFECT_REGISTRY[entry['name']]
    # 普通效果使用包含 eid 和词条序号的可读动态编号。穿甲/攻击上限
    # 默认使用固定的 3/4 取最高值；填写 stack 后改用动态编号正常叠加。
    effect_type = (
        effect_type if entry['stackable']
        else registry.get('effect_type', effect_type)
    )

    return EquipEffect(
        timer=timer,
        effect_type=effect_type,
        name=entry['name'],
        phase=_phase(entry['phase'] or registry['phase']),
        value=entry['value'],
        bias_or_weight=registry['bias_or_weight'],
    )


def _effect_skill(entries, effect_types):
    """根据一组最终普通词条动态创建一个 EquipSkill 子类。"""
    first_entry = entries[0]

    class ConfigEquipSkill(EquipSkill):
        def __init__(self, timer, master, value):
            super().__init__(timer, master, value)
            self.target = _target(master, first_entry['side'])
            self.buff = []
            if _conditions_active(master, first_entry['conditions']):
                self.buff.extend(
                    _effect_buff(timer, entry, effect_type)
                    for entry, effect_type in zip(entries, effect_types)
                )

    effect_label = '_'.join(str(effect_type) for effect_type in effect_types)
    ConfigEquipSkill.__name__ = f"ConfigEquipSkill_{effect_label}"
    return ConfigEquipSkill


def _python_skills(entry, eid, config):
    """包装现有 esid 技能，使配置中的参数、条件和目标仍可作用于它。"""
    module = importlib.import_module(
        f"src.skillCode.Equipment.esid{entry['esid']}"
    )
    result = []

    for base_skill in module.skill:
        conditions = entry['conditions']
        side = entry['side']
        configured_values = entry['values']

        class ConfigPythonSkill(base_skill):
            def __init__(self, timer, master, value):
                try:
                    values = configured_values if configured_values else value
                    super().__init__(timer, master, values)
                    if not _conditions_active(master, conditions):
                        self.buff = []
                    if side is not None:
                        self.target = _target(master, side)
                except EquipConfigError:
                    raise
                except Exception as exc:
                    raise EquipConfigError(
                        f"装备 {eid} 的特效配置错误: {exc}\n配置内容: {config}"
                    ) from exc

        ConfigPythonSkill.__name__ = f"ConfigPythonSkill_esid{entry['esid']}"
        result.append(ConfigPythonSkill)

    return result


def load_equip_config(config, eid='config'):
    """公开加载入口：转换为可写入 Equipment._skill 的技能类列表。"""
    try:
        parsed_entries = parse_equip_config(config)
        for entry in parsed_entries:
            _validate_entry(entry)

        skills = []
        effect_index = 0
        for entry in parsed_entries:
            if entry['kind'] == 'python':
                skills.extend(_python_skills(entry, eid, config))
            else:
                entries = entry['entries'] if entry['kind'] == 'group' else [entry]
                effect_types = []
                for _ in entries:
                    effect_index += 1
                    effect_types.append(ConfigEffectType(eid, effect_index))
                skills.append(_effect_skill(entries, effect_types))
        return skills
    except EquipConfigError:
        raise
    except Exception as exc:
        raise EquipConfigError(
            f"装备 {eid} 的特效配置错误: {exc}\n配置内容: {config}"
        ) from exc
